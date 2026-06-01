'''
Video Utilities Module
Helper functions for reading and writing video files.
'''

import cv2
import os


def read_video(video_path):
    '''Read a video file and return all frames as a list.'''
    if not os.path.exists(video_path):
        raise FileNotFoundError(f'Video not found: {video_path}')

    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    print(f'Read {len(frames)} frames from {video_path}')
    return frames


def save_video(output_frames, output_path, fps=24):
    '''Save a list of frames as a video file.'''
    if not output_frames:
        raise ValueError('No frames to save')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    height, width = output_frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in output_frames:
        out.write(frame)
    out.release()
    print(f'Saved video to {output_path} ({len(output_frames)} frames)')


def get_video_info(video_path):
    '''Get video metadata.'''
    cap = cv2.VideoCapture(video_path)
    info = {
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'total_frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
    }
    cap.release()
    return info
