'''
Football Tactical AI - Main Pipeline

Runs the full analysis:
  video -> detection -> tracking -> team classification
  -> tactical analysis -> LLM counter-strategy

Usage:
  python main.py --video data/input_videos/sample.mp4
  python main.py --demo    (runs with sample data, no video needed)
'''

import sys
import argparse
sys.path.insert(0, '.')

from analysis.tactical_analyzer import TacticalAnalyzer
from strategy.strategy_generator import StrategyGenerator


def run_demo():
    '''Run the strategy pipeline with sample tactical data (no video needed).'''
    print('=' * 60)
    print('FOOTBALL TACTICAL AI - DEMO MODE')
    print('=' * 60)

    # Sample opponent stats (as if computed from a real video)
    print()
    print('[1/2] Using sample opponent tactical data...')
    opponent_stats = {
        'formation': '4-3-3',
        'possession': 64,
        'playing_style': 'possession-based',
        'attack_side': 'right wing',
    }
    print(f'  {opponent_stats}')

    print()
    print('[2/2] Generating counter-strategy with LLM...')
    generator = StrategyGenerator()
    generator.load()
    result = generator.generate_counter_strategy(opponent_stats)

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
    print('=' * 60)
    print('Analysis complete!')


def run_full_pipeline(video_path):
    '''
    Run the complete pipeline on a real video.
    (Detection + tracking + teams + analysis + strategy)
    '''
    from utils.video_utils import read_video
    from trackers.tracker import Tracker
    from team_assigner.team_assigner import TeamAssigner

    print('=' * 60)
    print('FOOTBALL TACTICAL AI - FULL PIPELINE')
    print('=' * 60)

    print()
    print('[1/5] Reading video...')
    frames = read_video(video_path)

    print()
    print('[2/5] Detecting and tracking players...')
    tracker = Tracker('models/yolov8n.pt')
    tracks = tracker.get_object_tracks(
        frames, read_from_stub=True, stub_path='stubs/track_stubs.pkl'
    )

    print()
    print('[3/5] Assigning teams...')
    team_assigner = TeamAssigner()
    # Use first frame with players to set team colors
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
    print('[4/5] Analyzing tactics...')
    analyzer = TacticalAnalyzer(frame_width=frames[0].shape[1])
    # Simple possession placeholder: alternate (real calc needs ball assignment)
    team_ball_control = [1] * len(frames)
    opponent_stats = analyzer.build_team_stats(tracks, team_ball_control, team_id=1)
    print(f'  Detected: {opponent_stats}')

    print()
    print('[5/5] Generating counter-strategy...')
    generator = StrategyGenerator()
    generator.load()
    result = generator.generate_counter_strategy(opponent_stats)

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
