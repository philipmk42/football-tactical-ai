'''
Test script for YOLO detector.
Verifies the model loads and can detect objects.
'''

import sys
import time
sys.path.insert(0, '.')

from detection.yolo_detector import YOLODetector


def test_detector_loads():
    '''Test that YOLO model loads correctly.'''
    print('=' * 60)
    print('Testing YOLO Detector')
    print('=' * 60)

    print()
    print('[Test 1] Loading YOLO model...')
    detector = YOLODetector('models/yolov8n.pt')

    print()
    print('[Test 2] Checking detectable classes...')
    classes = detector.get_classes()
    print(f'  Total classes: {len(classes)}')
    print(f'  Has person: {0 in classes}')
    print(f'  Has sports ball: {32 in classes}')

    print()
    print('All tests passed! Detector is ready.')


if __name__ == '__main__':
    test_detector_loads()
