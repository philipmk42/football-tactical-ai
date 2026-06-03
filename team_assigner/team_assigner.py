'''
Team Assigner Module
Assigns players to one of two teams based on jersey color
using K-means clustering on the upper-body region of each player.
'''

from sklearn.cluster import KMeans
import numpy as np


class TeamAssigner:
    '''Classifies players into two teams by jersey color.'''

    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}
        self.kmeans = None

    def _get_clustering_model(self, image):
        '''Fit a 2-cluster KMeans on the pixels of an image region.'''
        image_2d = image.reshape(-1, 3)
        kmeans = KMeans(n_clusters=2, init='k-means++', n_init=1)
        kmeans.fit(image_2d)
        return kmeans

    def get_player_color(self, frame, bbox):
        '''Extract the dominant jersey color from a player's bounding box.'''
        x1, y1, x2, y2 = [int(v) for v in bbox]
        image = frame[y1:y2, x1:x2]

        # Use top half (jersey area, not shorts/legs)
        top_half = image[0:int(image.shape[0] / 2), :]

        kmeans = self._get_clustering_model(top_half)
        labels = kmeans.labels_
        clustered = labels.reshape(top_half.shape[0], top_half.shape[1])

        # The corners are likely background; the other cluster is the jersey
        corners = [
            clustered[0, 0], clustered[0, -1],
            clustered[-1, 0], clustered[-1, -1],
        ]
        background_cluster = max(set(corners), key=corners.count)
        player_cluster = 1 - background_cluster

        player_color = kmeans.cluster_centers_[player_cluster]
        return player_color

    def assign_team_colors(self, frame, player_detections):
        '''
        Determine the two team colors from all players in a frame.
        Call this once on a representative frame.
        '''
        player_colors = []
        for _, detection in player_detections.items():
            color = self.get_player_color(frame, detection['bbox'])
            player_colors.append(color)

        if len(player_colors) < 2:
            raise ValueError('Need at least 2 players to determine teams')

        kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10)
        kmeans.fit(player_colors)

        self.kmeans = kmeans
        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]
        print(f'Team colors assigned: {self.team_colors}')

    def get_player_team(self, frame, player_bbox, player_id):
        '''Return the team (1 or 2) for a given player.'''
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]

        player_color = self.get_player_color(frame, player_bbox)
        team_id = self.kmeans.predict(player_color.reshape(1, -1))[0]
        team_id += 1  # teams are 1 and 2, not 0 and 1

        self.player_team_dict[player_id] = team_id
        return team_id
