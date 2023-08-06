import pandas as pd
import numpy as np

from .Team import Team


class League():
    """League"""

    def __init__(self, season_files: np.array):
        self.games_df = pd.concat(
            (pd.read_csv(f) for f in season_files))
        self.teams = list(map(
            lambda name: Team(name, self.games_df), \
            self.games_df.home_team.unique()))

    def get_team(self, name: str):
        return next((x for x in self.teams if x.name == name), None)

    def get_opponent_winning_percentage_for_team_name(self, team_name: str, season: int):
        team = self.get_team(team_name)
        opponents = team.get_list_of_opponents(season)

        if len(opponents) == 0:
            return 0

        return np.array([
            self.get_team(o).winning_percentage_for_season(season) for o in opponents]) \
            .sum()/len(opponents)

    def print_teams_with_strength_of_schedule(self, season: int):
        for t in self.teams:
            print(self.get_opponent_winning_percentage_for_team_name(t.name, season))
