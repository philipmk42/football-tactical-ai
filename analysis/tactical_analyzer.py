'''
Tactical Analyzer Module
Converts raw tracking data into tactical statistics
(possession, formation estimate, attack side).
'''

import numpy as np


class TacticalAnalyzer:
    '''Computes tactical stats from tracking + team data.'''

    def __init__(self, frame_width=1920):
        self.frame_width = frame_width

    def calculate_possession(self, team_ball_control):
        '''Calculate possession percentage per team from ball control list.'''
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

    def calculate_possession_by_position(self, tracks):
        '''
        Fallback possession estimate based on which team has more
        players in the attacking half (used when ball detection is sparse).
        '''
        team1_count = 0
        team2_count = 0

        for frame_players in tracks['players']:
            for _, player in frame_players.items():
                team = player.get('team')
                if team == 1:
                    team1_count += 1
                elif team == 2:
                    team2_count += 1

        total = team1_count + team2_count
        if total == 0:
            return {1: 50, 2: 50}

        return {
            1: round((team1_count / total) * 100),
            2: round((team2_count / total) * 100),
        }

    def estimate_attack_side(self, tracks, team_id):
        '''Estimate attack side from average horizontal player position.'''
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
        '''Rough formation estimate based on player count.'''
        if num_players >= 10:
            return '4-3-3'
        elif num_players >= 8:
            return '4-4-2'
        elif num_players >= 6:
            return '4-2-1'
        else:
            return 'compact block'

    def build_team_stats(self, tracks, team_ball_control, team_id):
        '''Build the full team_stats dict for the strategy generator.'''
        possession = self.calculate_possession(team_ball_control)

        # If ball-based possession is unreliable (one team at 0),
        # fall back to position-based estimate.
        if possession.get(1, 0) == 0 or possession.get(2, 0) == 0:
            print('  Ball detection sparse - using position-based possession estimate')
            possession = self.calculate_possession_by_position(tracks)

        attack_side = self.estimate_attack_side(tracks, team_id)

        max_players = 0
        for frame_players in tracks['players']:
            count = sum(1 for p in frame_players.values()
                        if p.get('team') == team_id)
            max_players = max(max_players, count)

        formation = self.estimate_formation(max_players)

        team_possession = possession.get(team_id, 50)
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
