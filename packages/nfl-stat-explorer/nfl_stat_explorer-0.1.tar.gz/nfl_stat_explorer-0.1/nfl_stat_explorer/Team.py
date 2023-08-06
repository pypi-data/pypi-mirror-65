import pandas as pd
import numpy as np


class Team():
    """Team"""

    def __init__(self, name: str, games: pd.DataFrame):
        self.name = name
        self.games_df = games.loc[
            (games.home_team == name) |
            (games.away_team == name)]


    def winning_percentage_for_season(self, season: int):
        """Gives percentage of games won"""

        games = self.games_df.loc[(self.games_df.season == season)]

        home_wins = len(games.loc[
            (games.home_team == self.name) &
            (games.home_score >
            games.away_score)].index)

        away_wins = len(games.loc[
            (games.away_team == self.name) &
            (games.away_score >
            games.home_score)].index)

        total = len(self.games_df.loc[(self.games_df.season == season)].index)

        if total == 0:
            return -1
        return (home_wins + away_wins)/total


    def get_list_of_opponents(self, season: int):

        games = self.games_df.loc[(self.games_df.season == season)]
        if len(games) == 0:
            return []
        print(self.name + " getting list of opponents")
        print(games[['home_team','away_team']])

        return games[['home_team','away_team']] \
            .apply(lambda  x: x[0] if x[1] == self.name else x[1], axis=1) \
            .tolist()
