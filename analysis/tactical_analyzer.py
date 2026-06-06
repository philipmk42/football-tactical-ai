'''
Tactical Analyzer Module
Converts raw tracking data into tactical statistics
(possession, formation estimate, attack side) that feed
the strategy generator.
'''

import numpy as np


class TacticalAnalyzer:
    '''Computes tactical stats from tracking + team data.'''

    def __init__(self, frame_width=1920):
        self.frame_width = frame_width

    def calculate_possession(self, team_ball_control):
        '''
        Calculate possession percentage per team.

        Args:
            team_ball_control: list of team IDs (1 or 2) per frame
                               indicating which team had the ball

        Returns:
            dict {1: pct, 2: pct}
        '''
        if not team_ball_control:
            return {1: 0, 2: 0}

        arr = np.array(team_ball_control)
        total = len(arr)
        team1 = int(np.sum(arr == 1))
        team2 = int(np.sum(arr == 2))

        return {
            1: round((team1 / total) * 100),
            2: round((team2 / total) * 100),
        }

    def estimate_attack_side(self, tracks, team_id):
        '''
        Estimate which side a team attacks through based on
        average horizontal position of its players.

        Args:
            tracks: dict from the tracker
            team_id: which team to analyze (1 or 2)

        Returns:
            'left wing', 'central', or 'right wing'
        '''
        x_positions = []

        for frame_players in tracks['players']:
            for _, player in frame_players.items():
                if player.get('team') == team_id:
                    bbox = player['bbox']
                    center_x = (bbox[0] + bbox[2]) / 2
                    x_positions.append(center_x)

        if not x_positions:
            return 'central'

        avg_x = np.mean(x_positions)
        third = self.frame_width / 3

        if avg_x < third:
            return 'left wing'
        elif avg_x > 2 * third:
            return 'right wing'
        else:
            return 'central'

    def estimate_formation(self, num_players):
        '''
        Rough formation estimate based on player count.
        (A simple heuristic - real formation detection is complex.)

        Args:
            num_players: number of outfield players detected for a team

        Returns:
            formation string
        '''
        # Simple mapping; with 10 outfield players assume common shapes
        if num_players >= 10:
            return '4-3-3'
        elif num_players >= 8:
            return '4-4-2'
        elif num_players >= 6:
            return '4-2-1'
        else:
            return 'compact block'

    def build_team_stats(self, tracks, team_ball_control, team_id):
        '''
        Build the full team_stats dict expected by the strategy generator.

        Args:
            tracks: tracker output
            team_ball_control: per-frame possession list
            team_id: team to analyze

        Returns:
            dict with formation, possession, playing_style, attack_side
        '''
        possession = self.calculate_possession(team_ball_control)
        attack_side = self.estimate_attack_side(tracks, team_id)

        # Count max players seen for this team in any frame
        max_players = 0
        for frame_players in tracks['players']:
            count = sum(1 for p in frame_players.values()
                        if p.get('team') == team_id)
            max_players = max(max_players, count)

        formation = self.estimate_formation(max_players)

        # Infer style from possession
        team_possession = possession.get(team_id, 0)
        if team_possession > 55:
            style = 'possession-based'
        elif team_possession < 45:
            style = 'counter-attacking'
        else:
            style = 'balanced'

        return {
            'formation': formation,
            'possession': team_possession,
            'playing_style': style,
            'attack_side': attack_side,
        }
