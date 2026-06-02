'''
Tracker Module
Tracks players, referees, and ball across video frames using ByteTrack.
Assigns consistent IDs so each player can be followed frame-to-frame.
'''

from ultralytics import YOLO
import supervision as sv
import pickle
import os


class Tracker:
    '''Multi-object tracker built on YOLO + ByteTrack.'''

    def __init__(self, model_path='models/yolov8n.pt'):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f'Model not found: {model_path}')
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
        print(f'Tracker initialized with model: {model_path}')

    def detect_frames(self, frames, batch_size=20):
        '''Run YOLO detection on all frames in batches.'''
        detections = []
        for i in range(0, len(frames), batch_size):
            batch = frames[i:i + batch_size]
            batch_detections = self.model.predict(batch, conf=0.1, verbose=False)
            detections += batch_detections
        return detections

    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        '''
        Detect and track objects across frames.
        Returns a dict with tracked positions per frame for players, referees, ball.
        '''
        if read_from_stub and stub_path and os.path.exists(stub_path):
            with open(stub_path, 'rb') as f:
                print(f'Loading tracks from cache: {stub_path}')
                return pickle.load(f)

        detections = self.detect_frames(frames)

        tracks = {
            'players': [],
            'referees': [],
            'ball': [],
        }

        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v: k for k, v in cls_names.items()}

            detection_sv = sv.Detections.from_ultralytics(detection)
            detection_with_tracks = self.tracker.update_with_detections(detection_sv)

            tracks['players'].append({})
            tracks['referees'].append({})
            tracks['ball'].append({})

            for frame_detection in detection_with_tracks:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]
                track_id = frame_detection[4]

                if cls_id == cls_names_inv.get('person'):
                    tracks['players'][frame_num][track_id] = {'bbox': bbox}

            for frame_detection in detection_sv:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]

                if cls_id == cls_names_inv.get('sports ball'):
                    tracks['ball'][frame_num][1] = {'bbox': bbox}

        if stub_path:
            with open(stub_path, 'wb') as f:
                pickle.dump(tracks, f)
            print(f'Tracks saved to: {stub_path}')

        return tracks
