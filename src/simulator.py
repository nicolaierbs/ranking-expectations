from logger import logger
import pandas as pd
import random

def guess_points(series):
    #Guess the points of a team based on the Ballpunkte statistics
    return random.gauss(series["mean"], series["std"])


def simulate_set(df_team_point_statistics, team1, team2):
    #Simulate a set based on the Ballpunkte statistics of the teams
    team1_ballpunkte = guess_points(df_team_point_statistics.loc[team1, :])
    team2_ballpunkte = guess_points(df_team_point_statistics.loc[team2, :])

    factor = 25/max(team1_ballpunkte, team2_ballpunkte)
    team1_ballpunkte = int(team1_ballpunkte * factor)
    team2_ballpunkte = int(team2_ballpunkte * factor)
    if team1_ballpunkte == team2_ballpunkte:
        team2_ballpunkte -= 1
    return team1_ballpunkte, team2_ballpunkte

def simulate_future_games(df_future, df_team_point_statistics):
    #Simulate the outcome of the future games based on the Ballpunkte statistics of the teams
    logger.debug("Simulating future games")
    df_future = df_future.copy()
    for index, row in df_future.iterrows():
        team1 = row["Mannschaft 1"]
        team2 = row["Mannschaft 2"]
        #Calculate the expected points for a team
        expected_difference = df_team_point_statistics.loc[team1, "mean"] - df_team_point_statistics.loc[team2, "mean"]

        team1_sets_won = 0
        team2_sets_won = 0
        for i in range(1, 6):
            team1_ballpunkte, team2_ballpunkte = simulate_set(df_team_point_statistics, team1, team2)
            if team1_ballpunkte > team2_ballpunkte:
                team1_sets_won += 1
            else:
                team2_sets_won += 1
            if max(team1_sets_won, team1_sets_won) <=3:
                df_future.at[index, f"Satz {i} - Ballpunkte 1"] = team1_ballpunkte
                df_future.at[index, f"Satz {i} - Ballpunkte 2"] = team2_ballpunkte
            else:
                df_future.at[index, f"Satz {i} - Ballpunkte 1"] = pd.NA
                df_future.at[index, f"Satz {i} - Ballpunkte 2"] = pd.NA

    return df_future