'''
Test script for Tracker.
Verifies the tracker initializes and processes frames without errors.
'''

import sys
import numpy as np
sys.path.insert(0, '.')

from trackers.tracker import Tracker


def test_tracker():
    '''Test tracker on synthetic frames.'''
    print('=' * 60)
    print('Testing Tracker')
    print('=' * 60)

    print()
    print('[Test 1] Initializing tracker...')
    tracker = Tracker('models/yolov8n.pt')

    print()
    print('[Test 2] Creating synthetic test frames...')
    frames = [np.zeros((640, 640, 3), dtype=np.uint8) for _ in range(3)]
    print(f'  Created {len(frames)} test frames')

    print()
    print('[Test 3] Running tracking...')
    tracks = tracker.get_object_tracks(frames)

    print()
    print('[Test 4] Verifying output structure...')
    assert 'players' in tracks, 'Missing players key'
    assert 'referees' in tracks, 'Missing referees key'
    assert 'ball' in tracks, 'Missing ball key'
    assert len(tracks['players']) == 3, 'Should have 3 frames of player data'

    players_per_frame = [len(f) for f in tracks['players']]
    ball_per_frame = [len(f) for f in tracks['ball']]

    print('  Output structure valid')
    print(f'  Players tracked per frame: {players_per_frame}')
    print(f'  Ball detected per frame: {ball_per_frame}')

    print()
    print('All tests passed! Tracker is working.')


if __name__ == '__main__':
    test_tracker()
