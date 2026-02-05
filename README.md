# AI-Powered Retail Store Analytics

Animated React experience showcasing an AI/ML hackathon project for retail store analytics using computer vision.

## Tech
- React + Vite
- TailwindCSS
- Framer Motion

## Development
```bash
npm install
npm run dev
```

## Computer Vision Retail Analytics (Python)
`retail_analytics.py` processes recorded or live CCTV video streams to detect people, track them with unique IDs, count entries/exits, and generate movement paths and heatmaps.

### Features
- YOLOv8 person detection (real-time)
- DeepSORT multi-object tracking
- Virtual line-based entry/exit counting
- Customer movement trajectories
- Heatmap visualization for high-traffic/dwell areas
- Annotated video output with IDs and overlays

### Usage
```bash
python retail_analytics.py \
  --source path/to/video.mp4 \
  --output outputs/annotated.mp4 \
  --heatmap-output outputs/heatmap.png \
  --line 100 200 500 200 \
  --entry-positive
```

For live feeds, pass a camera index or RTSP URL:
```bash
python retail_analytics.py --source 0 --display
```

### Dependencies
```bash
pip install ultralytics deep-sort-realtime opencv-python numpy
```
