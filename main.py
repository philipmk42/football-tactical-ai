'''
Football Tactical AI - Main Pipeline

video -> detection -> tracking -> team classification
-> ball possession -> tactical analysis -> LLM counter-strategy -> report
'''

import sys
import argparse
sys.path.insert(0, '.')

from analysis.tactical_analyzer import TacticalAnalyzer
from strategy.strategy_generator import StrategyGenerator
from reporting.report_generator import generate_report


def run_demo():
    '''Run the strategy pipeline with sample tactical data (no video needed).'''
    print('=' * 60)
    print('FOOTBALL TACTICAL AI - DEMO MODE')
    print('=' * 60)

    print()
    print('[1/3] Using sample opponent tactical data...')
    opponent_stats = {
        'formation': '4-3-3',
        'possession': 64,
        'playing_style': 'possession-based',
        'attack_side': 'right wing',
    }
    print(f'  {opponent_stats}')

    print()
    print('[2/3] Generating counter-strategy with LLM...')
    generator = StrategyGenerator()
    generator.load()
    result = generator.generate_counter_strategy(opponent_stats)

    print()
    print('[3/3] Saving report...')
    report_path = generate_report(result['situation'], result['counter_strategy'])

    print()
    print('=' * 60)
    print('TACTICAL ANALYSIS REPORT')
    print('=' * 60)
    print()
    print('OPPONENT SITUATION:')
    print(result['situation'])
    print()
    print('RECOMMENDED COUNTER-STRATEGY:')
    print(result['counter_strategy'])
    print()
    print(f'Full report saved to: {report_path}')
    print('Analysis complete!')


def run_full_pipeline(video_path):
    '''Run the complete pipeline on a real video.'''
    from utils.video_utils import read_video
    from trackers.tracker import Tracker
    from team_assigner.team_assigner import TeamAssigner
    from player_ball_assigner.player_ball_assigner import PlayerBallAssigner

    print('=' * 60)
    print('FOOTBALL TACTICAL AI - FULL PIPELINE')
    print('=' * 60)

    print()
    print('[1/6] Reading video...')
    frames = read_video(video_path)

    print()
    print('[2/6] Detecting and tracking players...')
    tracker = Tracker('models/yolov8n.pt')
    tracks = tracker.get_object_tracks(
        frames, read_from_stub=True, stub_path='stubs/track_stubs.pkl'
    )

    print()
    print('[3/6] Assigning teams...')
    team_assigner = TeamAssigner()
    first_frame_players = tracks['players'][0]
    if first_frame_players:
        team_assigner.assign_team_colors(frames[0], first_frame_players)
        for frame_num, player_track in enumerate(tracks['players']):
            for player_id, track in player_track.items():
                team = team_assigner.get_player_team(
                    frames[frame_num], track['bbox'], player_id
                )
                tracks['players'][frame_num][player_id]['team'] = team

    print()
    print('[4/6] Calculating ball possession...')
    ball_assigner = PlayerBallAssigner()
    team_ball_control = []
    last_team = 1
    for frame_num, player_track in enumerate(tracks['players']):
        ball_frame = tracks['ball'][frame_num]
        if ball_frame and 1 in ball_frame:
            ball_bbox = ball_frame[1]['bbox']
            assigned_player = ball_assigner.assign_ball_to_player(
                player_track, ball_bbox
            )
            if assigned_player != -1:
                last_team = player_track[assigned_player].get('team', last_team)
        team_ball_control.append(last_team)

    print(f'  Frames with possession data: {len(team_ball_control)}')

    print()
    print('[5/6] Analyzing tactics...')
    analyzer = TacticalAnalyzer(frame_width=frames[0].shape[1])
    opponent_stats = analyzer.build_team_stats(tracks, team_ball_control, team_id=1)
    print(f'  Detected: {opponent_stats}')

    print()
    print('[6/6] Generating counter-strategy...')
    generator = StrategyGenerator()
    generator.load()
    result = generator.generate_counter_strategy(opponent_stats)

    report_path = generate_report(result['situation'], result['counter_strategy'])

    print()
    print('=' * 60)
    print('TACTICAL ANALYSIS REPORT')
    print('=' * 60)
    print()
    print('OPPONENT SITUATION:')
    print(result['situation'])
    print()
    print('RECOMMENDED COUNTER-STRATEGY:')
    print(result['counter_strategy'])
    print()
    print(f'Full report saved to: {report_path}')
    print('Analysis complete!')


def main():
    parser = argparse.ArgumentParser(description='Football Tactical AI')
    parser.add_argument('--video', type=str, help='Path to input video')
    parser.add_argument('--demo', action='store_true', help='Run demo mode')
    args = parser.parse_args()

    if args.demo or not args.video:
        run_demo()
    else:
        run_full_pipeline(args.video)


if __name__ == '__main__':
    main()
