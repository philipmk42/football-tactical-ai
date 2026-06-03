'''
Test script for TeamAssigner.
Creates synthetic players with two jersey colors and verifies
K-means separates them into two teams.
'''

import sys
import numpy as np
sys.path.insert(0, '.')

from team_assigner.team_assigner import TeamAssigner


def test_team_assigner():
    '''Test team assignment on synthetic colored players.'''
    print('=' * 60)
    print('Testing Team Assigner')
    print('=' * 60)

    print()
    print('[Test 1] Creating synthetic frame with two team colors...')
    # Blank frame
    frame = np.zeros((640, 640, 3), dtype=np.uint8)

    # Draw 4 'players': 2 red (team 1), 2 blue (team 2)
    # Red players (BGR: blue=0, green=0, red=255)
    frame[100:200, 100:160] = [0, 0, 255]
    frame[100:200, 300:360] = [0, 0, 255]
    # Blue players (BGR: blue=255, green=0, red=0)
    frame[400:500, 100:160] = [255, 0, 0]
    frame[400:500, 300:360] = [255, 0, 0]

    # Define their bounding boxes
    player_detections = {
        1: {'bbox': [100, 100, 160, 200]},  # red
        2: {'bbox': [300, 100, 360, 200]},  # red
        3: {'bbox': [100, 400, 160, 500]},  # blue
        4: {'bbox': [300, 400, 360, 500]},  # blue
    }
    print('  Created 4 players (2 red, 2 blue)')

    print()
    print('[Test 2] Initializing team assigner...')
    assigner = TeamAssigner()

    print()
    print('[Test 3] Assigning team colors...')
    assigner.assign_team_colors(frame, player_detections)

    print()
    print('[Test 4] Classifying each player...')
    results = {}
    for player_id, detection in player_detections.items():
        team = assigner.get_player_team(frame, detection['bbox'], player_id)
        results[player_id] = team
        print(f'  Player {player_id}: Team {team}')

    print()
    print('[Test 5] Verifying red players share a team, blue share another...')
    assert results[1] == results[2], 'Red players should be same team'
    assert results[3] == results[4], 'Blue players should be same team'
    assert results[1] != results[3], 'Red and blue should be different teams'

    print('  Teams correctly separated!')
    print()
    print('All tests passed! Team Assigner is working.')


if __name__ == '__main__':
    test_team_assigner()
