import argparse
import collections
import time
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Tuple

import cv2
import numpy as np

try:
    from ultralytics import YOLO
except ImportError:  # pragma: no cover - optional dependency
    YOLO = None

try:
    from deep_sort_realtime.deepsort_tracker import DeepSort
except ImportError:  # pragma: no cover - optional dependency
    DeepSort = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retail analytics with CV detection + tracking")
    parser.add_argument("--source", required=True, help="Video file path or camera index")
    parser.add_argument("--model", default="yolov8n.pt", help="YOLOv8 model path")
    parser.add_argument("--output", default="annotated_output.mp4", help="Annotated video output")
    parser.add_argument("--heatmap", default="heatmap.png", help="Heatmap image output")
    parser.add_argument("--line", default="0.5,0.6,0.5,0.2", help="Line x1,y1,x2,y2 as relative ratios")
    parser.add_argument("--conf", type=float, default=0.35, help="Detection confidence threshold")
    parser.add_argument("--max-age", type=int, default=30, help="Tracker max age")
    parser.add_argument("--display", action="store_true", help="Show live window")
    return parser.parse_args()


@dataclass
class TrackInfo:
    centroid_history: Deque[Tuple[int, int]]
    last_side: Optional[int] = None
    counted: bool = False


class LineCounter:
    def __init__(self, start: Tuple[int, int], end: Tuple[int, int]):
        self.start = start
        self.end = end
        self.in_count = 0
        self.out_count = 0

    def _side(self, point: Tuple[int, int]) -> int:
        x1, y1 = self.start
        x2, y2 = self.end
        px, py = point
        value = (x2 - x1) * (py - y1) - (y2 - y1) * (px - x1)
        return 1 if value > 0 else -1

    def update(self, track_id: int, point: Tuple[int, int], info: TrackInfo) -> None:
        current_side = self._side(point)
        if info.last_side is None:
            info.last_side = current_side
            return
        if info.last_side != current_side and not info.counted:
            if current_side > info.last_side:
                self.in_count += 1
            else:
                self.out_count += 1
            info.counted = True
        info.last_side = current_side


class Heatmap:
    def __init__(self, frame_size: Tuple[int, int]):
        self.height, self.width = frame_size
        self.accumulator = np.zeros((self.height, self.width), dtype=np.float32)

    def add_point(self, point: Tuple[int, int]) -> None:
        x, y = point
        if 0 <= x < self.width and 0 <= y < self.height:
            cv2.circle(self.accumulator, (x, y), 18, 1.0, -1)

    def render(self, frame: np.ndarray, alpha: float = 0.45) -> np.ndarray:
        normalized = cv2.normalize(self.accumulator, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        colored = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)
        return cv2.addWeighted(frame, 1 - alpha, colored, alpha, 0)

    def save(self, path: str) -> None:
        normalized = cv2.normalize(self.accumulator, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        colored = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)
        cv2.imwrite(path, colored)


class RetailAnalytics:
    def __init__(
        self,
        model_path: str,
        line: Tuple[float, float, float, float],
        conf: float,
        max_age: int,
    ) -> None:
        if YOLO is None:
            raise RuntimeError("ultralytics is required for YOLOv8 detection")
        if DeepSort is None:
            raise RuntimeError("deep-sort-realtime is required for tracking")
        self.model = YOLO(model_path)
        self.tracker = DeepSort(max_age=max_age)
        self.conf = conf
        self.line_ratios = line
        self.track_state: Dict[int, TrackInfo] = {}
        self.line_counter: Optional[LineCounter] = None
        self.heatmap: Optional[Heatmap] = None
        self.people_count = 0

    def _init_helpers(self, frame: np.ndarray) -> None:
        height, width = frame.shape[:2]
        x1, y1, x2, y2 = self.line_ratios
        start = (int(x1 * width), int(y1 * height))
        end = (int(x2 * width), int(y2 * height))
        self.line_counter = LineCounter(start, end)
        self.heatmap = Heatmap((height, width))

    def _detect(self, frame: np.ndarray) -> List[Tuple[List[float], float, str]]:
        results = self.model(frame, verbose=False)[0]
        detections = []
        for box, score, cls_id in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
            if score < self.conf:
                continue
            label = self.model.names[int(cls_id)]
            if label != "person":
                continue
            x1, y1, x2, y2 = box.tolist()
            detections.append(([x1, y1, x2, y2], float(score), label))
        return detections

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        if self.line_counter is None or self.heatmap is None:
            self._init_helpers(frame)
        assert self.line_counter is not None
        assert self.heatmap is not None

        detections = self._detect(frame)
        tracks = self.tracker.update_tracks(detections, frame=frame)
        self.people_count = 0

        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            ltrb = track.to_ltrb()
            x1, y1, x2, y2 = map(int, ltrb)
            centroid = (int((x1 + x2) / 2), int((y1 + y2) / 2))
            info = self.track_state.setdefault(
                track_id, TrackInfo(centroid_history=collections.deque(maxlen=30))
            )
            info.centroid_history.append(centroid)
            self.line_counter.update(track_id, centroid, info)
            self.heatmap.add_point(centroid)
            self.people_count += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), (64, 243, 255), 2)
            cv2.putText(
                frame,
                f"ID {track_id}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            for idx in range(1, len(info.centroid_history)):
                cv2.line(
                    frame,
                    info.centroid_history[idx - 1],
                    info.centroid_history[idx],
                    (124, 58, 237),
                    2,
                )

        start = self.line_counter.start
        end = self.line_counter.end
        cv2.line(frame, start, end, (255, 255, 0), 2)
        overlay = self.heatmap.render(frame)
        stats = (
            f"Live Count: {self.people_count} | In: {self.line_counter.in_count} | Out: {self.line_counter.out_count}"
        )
        cv2.putText(
            overlay,
            stats,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        return overlay

    def finalize_heatmap(self, path: str) -> None:
        if self.heatmap is None:
            return
        self.heatmap.save(path)


def open_source(source: str) -> cv2.VideoCapture:
    if source.isdigit():
        return cv2.VideoCapture(int(source))
    return cv2.VideoCapture(source)


def main() -> None:
    args = parse_args()
    x1, y1, x2, y2 = (float(v) for v in args.line.split(","))
    analytics = RetailAnalytics(args.model, (x1, y1, x2, y2), args.conf, args.max_age)
    capture = open_source(args.source)
    if not capture.isOpened():
        raise RuntimeError("Unable to open source")

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS) or 30
    writer = cv2.VideoWriter(
        args.output,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    last_log = time.time()
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        annotated = analytics.process_frame(frame)
        writer.write(annotated)
        if args.display:
            cv2.imshow("Retail Analytics", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        if time.time() - last_log > 2:
            print(
                f"Live Count: {analytics.people_count} | In: {analytics.line_counter.in_count} | "
                f"Out: {analytics.line_counter.out_count}"
            )
            last_log = time.time()

    capture.release()
    writer.release()
    analytics.finalize_heatmap(args.heatmap)
    if args.display:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
