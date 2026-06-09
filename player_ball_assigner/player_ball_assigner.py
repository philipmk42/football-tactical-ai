'''
Player Ball Assigner Module
Determines which player is in possession of the ball each frame
by finding the player closest to the ball.
'''

import sys
sys.path.insert(0, '.')

from utils.bbox_utils import get_center_of_bbox, measure_distance


class PlayerBallAssigner:
    '''Assigns ball possession to the nearest player.'''

    def __init__(self, max_distance=70):
        self.max_distance = max_distance

    def assign_ball_to_player(self, players, ball_bbox):
        '''
        Find which player has the ball in a single frame.

        Args:
            players: dict of {player_id: {'bbox': [...], 'team': N}}
            ball_bbox: bounding box of the ball

        Returns:
            player_id of the closest player within range, or -1 if none
        '''
        ball_position = get_center_of_bbox(ball_bbox)

        minimum_distance = 99999
        assigned_player = -1

        for player_id, player in players.items():
            player_bbox = player['bbox']
            dist_left = measure_distance(
                (player_bbox[0], player_bbox[3]), ball_position
            )
            dist_right = measure_distance(
                (player_bbox[2], player_bbox[3]), ball_position
            )
            distance = min(dist_left, dist_right)

            if distance < self.max_distance and distance < minimum_distance:
                minimum_distance = distance
                assigned_player = player_id

        return assigned_player
