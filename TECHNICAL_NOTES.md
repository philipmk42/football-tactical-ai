# 📐 Technical Notes

## Architecture Decisions

### Why TinyLlama over Phi-3?
- Optimized for CPU inference (no GPU required)
- Faster generation on limited hardware (8GB RAM)
- 1.1B parameters vs 3.8B - better for prototyping
- Can upgrade to larger models when GPU available

### Why YOLOv8?
- State-of-the-art object detection
- Pre-trained models available
- Fast inference
- Easy integration via Ultralytics

### Why K-means for Team Classification?
- Unsupervised - no labeled data needed
- Effective for jersey color separation
- Fast computation
- Works with 2 distinct team colors

## Pipeline Flow
