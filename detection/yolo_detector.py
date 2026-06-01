'''
YOLO Detector Module
Detects players, ball, and other objects in football frames.
'''

from ultralytics import YOLO
import os


class YOLODetector:
    '''YOLO-based object detector.'''

    def __init__(self, model_path='models/yolov8n.pt'):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'Model not found: {model_path}')
        self.model_path = model_path
        self.model = YOLO(model_path)
        print(f'YOLO model loaded: {model_path}')
        print(f'Classes: {self.model.names}')

    def detect_frame(self, frame, conf=0.25):
        '''Detect objects in a single frame.'''
        results = self.model.predict(frame, conf=conf, verbose=False)
        return results[0]

    def detect_video(self, frames, conf=0.25, batch_size=20):
        '''Detect objects across multiple frames.'''
        detections = []
        total = len(frames)
        print(f'Running detection on {total} frames...')
        for i in range(0, total, batch_size):
            batch = frames[i:i + batch_size]
            batch_results = self.model.predict(batch, conf=conf, verbose=False)
            detections.extend(batch_results)
            progress = min(i + batch_size, total)
            print(f'  Processed {progress}/{total} frames')
        return detections

    def get_classes(self):
        '''Return the class names YOLO can detect.'''
        return self.model.names
