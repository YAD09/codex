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

## Computer Vision Pipeline
Requires Python dependencies: `ultralytics`, `deep-sort-realtime`, `opencv-python`, `numpy`.

```bash
python python/retail_analytics.py --source path/to/video.mp4 --model yolov8n.pt --display
```

Outputs:
- Annotated video with bounding boxes + IDs (default: `annotated_output.mp4`)
- Heatmap image (default: `heatmap.png`)
- Console live count + entry/exit statistics
