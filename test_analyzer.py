'''
Test script for TacticalAnalyzer.
Feeds synthetic tracking data and verifies tactical stats are computed.
'''

import sys
sys.path.insert(0, '.')

from analysis.tactical_analyzer import TacticalAnalyzer


def test_analyzer():
    '''Test tactical analysis on synthetic tracking data.'''
    print('=' * 60)
    print('Testing Tactical Analyzer')
    print('=' * 60)

    print()
    print('[Test 1] Initializing analyzer...')
    analyzer = TacticalAnalyzer(frame_width=1920)

    print()
    print('[Test 2] Testing possession calculation...')
    # Team 1 has ball 6 frames, team 2 has it 4 frames
    ball_control = [1, 1, 1, 2, 2, 1, 1, 2, 2, 1]
    possession = analyzer.calculate_possession(ball_control)
    print(f'  Possession: {possession}')
    assert possession[1] == 60, 'Team 1 should have 60%'
    assert possession[2] == 40, 'Team 2 should have 40%'
    print('  Possession correct')

    print()
    print('[Test 3] Building synthetic tracks...')
    # 2 frames, team 1 players on right side (high x), team 2 on left
    tracks = {
        'players': [
            {
                1: {'bbox': [1400, 300, 1450, 400], 'team': 1},
                2: {'bbox': [1500, 300, 1550, 400], 'team': 1},
                3: {'bbox': [200, 300, 250, 400], 'team': 2},
            },
            {
                1: {'bbox': [1420, 300, 1470, 400], 'team': 1},
                2: {'bbox': [1520, 300, 1570, 400], 'team': 1},
                3: {'bbox': [220, 300, 270, 400], 'team': 2},
            },
        ],
        'referees': [{}, {}],
        'ball': [{}, {}],
    }
    print('  Created 2 frames of tracking data')

    print()
    print('[Test 4] Testing attack side estimation...')
    side1 = analyzer.estimate_attack_side(tracks, team_id=1)
    side2 = analyzer.estimate_attack_side(tracks, team_id=2)
    print(f'  Team 1 attack side: {side1}')
    print(f'  Team 2 attack side: {side2}')
    assert side1 == 'right wing', 'Team 1 is on the right'
    assert side2 == 'left wing', 'Team 2 is on the left'
    print('  Attack sides correct')

    print()
    print('[Test 5] Building full team stats...')
    stats = analyzer.build_team_stats(tracks, ball_control, team_id=1)
    print(f'  Team 1 stats: {stats}')
    assert 'formation' in stats
    assert 'possession' in stats
    assert 'playing_style' in stats
    assert 'attack_side' in stats
    print('  Full stats structure valid')

    print()
    print('All tests passed! Tactical Analyzer is working.')


if __name__ == '__main__':
    test_analyzer()
