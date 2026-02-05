#!/usr/bin/env python3
"""Retail analytics system with YOLOv8 + DeepSORT."""
from __future__ import annotations

import argparse
import sys
import time
from collections import defaultdict, deque
from pathlib import Path

import cv2
import numpy as np

try:
    from ultralytics import YOLO
except ImportError as exc:
    raise SystemExit(
        "Ultralytics YOLOv8 is required. Install with `pip install ultralytics`."
    ) from exc

try:
    from deep_sort_realtime.deepsort_tracker import DeepSort
except ImportError as exc:
    raise SystemExit(
        "deep-sort-realtime is required. Install with `pip install deep-sort-realtime`."
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retail analytics with YOLOv8 + DeepSORT")
    parser.add_argument(
        "--source",
        default=0,
        help="Video source (file path, RTSP URL, or camera index).",
    )
    parser.add_argument("--output", default="outputs/annotated.mp4", help="Output video path.")
    parser.add_argument(
        "--heatmap-output",
        default="outputs/heatmap.png",
        help="Heatmap image output path.",
    )
    parser.add_argument("--model", default="yolov8n.pt", help="YOLOv8 model path.")
    parser.add_argument("--conf", type=float, default=0.35, help="Confidence threshold.")
    parser.add_argument(
        "--line",
        nargs=4,
        type=int,
        metavar=("X1", "Y1", "X2", "Y2"),
        default=[100, 200, 500, 200],
        help="Counting line endpoints.",
    )
    parser.add_argument(
        "--entry-positive",
        action="store_true",
        help="Treat crossing from negative to positive side as entry.",
    )
    parser.add_argument(
        "--display",
        action="store_true",
        help="Display live window while processing.",
    )
    parser.add_argument(
        "--max-trail",
        type=int,
        default=30,
        help="Maximum trail length for each track.",
    )
    return parser.parse_args()


def ensure_parent(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def line_side(point: tuple[int, int], p1: tuple[int, int], p2: tuple[int, int]) -> float:
    x, y = point
    x1, y1 = p1
    x2, y2 = p2
    return (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)


def draw_label(frame: np.ndarray, text: str, origin: tuple[int, int]) -> None:
    cv2.rectangle(frame, (origin[0] - 5, origin[1] - 18), (origin[0] + 180, origin[1] + 5), (0, 0, 0), -1)
    cv2.putText(frame, text, origin, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


def main() -> None:
    args = parse_args()

    source = int(args.source) if str(args.source).isdigit() else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise SystemExit(f"Unable to open video source: {args.source}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    ensure_parent(args.output)
    ensure_parent(args.heatmap_output)

    writer = cv2.VideoWriter(
        args.output,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    model = YOLO(args.model)
    tracker = DeepSort(max_age=30, n_init=2, nms_max_overlap=1.0, max_cosine_distance=0.3)

    p1 = (args.line[0], args.line[1])
    p2 = (args.line[2], args.line[3])
    entry_positive = args.entry_positive

    track_history: dict[int, deque[tuple[int, int]]] = defaultdict(
        lambda: deque(maxlen=args.max_trail)
    )
    last_side: dict[int, float] = {}
    entry_count = 0
    exit_count = 0
    heatmap = np.zeros((height, width), dtype=np.float32)

    start_time = time.time()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        results = model(frame, conf=args.conf, verbose=False)[0]
        detections = []
        for box in results.boxes:
            cls = int(box.cls.item())
            if cls != 0:
                continue
            conf = float(box.conf.item())
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            w, h = x2 - x1, y2 - y1
            detections.append(([x1, y1, w, h], conf, "person"))

        tracks = tracker.update_tracks(detections, frame=frame)
        active_ids = set()

        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            active_ids.add(track_id)
            x1, y1, x2, y2 = map(int, track.to_tlbr())
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

            track_history[track_id].append((cx, cy))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"ID {track_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

            if len(track_history[track_id]) > 1:
                pts = np.array(track_history[track_id], dtype=np.int32)
                cv2.polylines(frame, [pts], False, (255, 200, 0), 2)

            heatmap = cv2.circle(heatmap, (cx, cy), 8, 1.0, -1)

            current_side = line_side((cx, cy), p1, p2)
            previous_side = last_side.get(track_id)
            if previous_side is not None and current_side == 0:
                current_side = previous_side
            if previous_side is not None and np.sign(previous_side) != np.sign(current_side):
                if entry_positive:
                    if previous_side < 0 and current_side > 0:
                        entry_count += 1
                    else:
                        exit_count += 1
                else:
                    if previous_side > 0 and current_side < 0:
                        entry_count += 1
                    else:
                        exit_count += 1
            last_side[track_id] = current_side

        cv2.line(frame, p1, p2, (255, 0, 255), 2)

        live_count = len(active_ids)
        elapsed = max(time.time() - start_time, 1e-5)
        fps_estimate = frame_count / elapsed

        draw_label(frame, f"Live count: {live_count}", (10, 30))
        draw_label(frame, f"Entries: {entry_count}  Exits: {exit_count}", (10, 55))
        draw_label(frame, f"FPS: {fps_estimate:.1f}", (10, 80))

        normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        colored = cv2.applyColorMap(normalized.astype(np.uint8), cv2.COLORMAP_JET)
        overlay = cv2.addWeighted(frame, 0.7, colored, 0.3, 0)

        writer.write(overlay)

        if args.display:
            cv2.imshow("Retail Analytics", overlay)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    writer.release()
    if args.display:
        cv2.destroyAllWindows()

    normalized = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    colored = cv2.applyColorMap(normalized.astype(np.uint8), cv2.COLORMAP_JET)
    cv2.imwrite(args.heatmap_output, colored)

    print("Processing complete.")
    print(f"Annotated video saved to: {args.output}")
    print(f"Heatmap saved to: {args.heatmap_output}")
    print(f"Entries: {entry_count} | Exits: {exit_count} | Live count: {live_count}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
