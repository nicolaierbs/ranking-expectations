from collections import defaultdict
from statistics import mean, stdev
import pandas as pd


def match_points(sets_diff):
    if sets_diff > 1:
        return 3
    elif sets_diff == 1:
        return 2
    elif sets_diff == -1:
        return 1
    else:
        return 0


def team_point_statistics(games_df):
    teams = defaultdict(list)
    #Iterate over all rows in the dataframe and calculate for each Satz the difference in Ballpunkte between the two teams. Add the difference to the list of the respective team
    for index, row in games_df.iterrows():
        team1 = row["Mannschaft 1"]
        team2 = row["Mannschaft 2"]

        for i in range(1, 5):
            difference = row[f"Satz {i} - Ballpunkte 1"] - row[f"Satz {i} - Ballpunkte 2"]
            # check if the difference is not NaN
            if not pd.isna(difference):
                teams[team1].append(difference)
                teams[team2].append(-difference)

    #Calculate the mean and standard deviation of the Ballpunkte differences for each team and store it in a dataframe
    statistics = dict()
    for team, points in teams.items():
        statistics[team] = {
            "mean": mean(points),
            "std": stdev(points)
        }

    # return teams statistics as a dataframe
    return pd.DataFrame(statistics).T

def team_statistics(games_df):
    results = list()
    #Iterate over all rows in the dataframe and calculate for each Satz the difference in Ballpunkte between the two teams. Add the difference to the list of the respective team
    for index, row in games_df.iterrows():
        team1 = row["Mannschaft 1"]
        team2 = row["Mannschaft 2"]

        team1_sets = 0
        team2_sets = 0
        team1_points = 0
        team2_points = 0

        for i in range(1, 6):
            difference = row[f"Satz {i} - Ballpunkte 1"] - row[f"Satz {i} - Ballpunkte 2"]
            # check if the difference is not NaN
            if not pd.isna(difference):
                team1_points += row[f"Satz {i} - Ballpunkte 1"] 
                team2_points += row[f"Satz {i} - Ballpunkte 2"]
                if difference > 0:
                    team1_sets += 1
                else:
                    team2_sets += 1

        result1 = dict()
        result1["Mannschaft"] = team1
        result1["Punkte"] = match_points(team1_sets - team2_sets)
        result1["Gewonnene Sätze"] = team1_sets
        result1["Verlorene Sätze"] = team2_sets
        result1["Gewonnene Ballpunkte"] = team1_points
        result1["Verlorene Ballpunkte"] = team2_points
        #Return 0 if the difference of team1_sets and team2_sets is lower than 2, return 1 if the difference is 1, 2 if the difference is 2 and 3 if the difference is higher than 2
        results.append(result1)

        result2 = dict()
        result2["Mannschaft"] = team2
        result2["Punkte"] = match_points(team2_sets - team1_sets)
        result2["Gewonnene Sätze"] = team2_sets
        result2["Verlorene Sätze"] = team1_sets
        result2["Gewonnene Ballpunkte"] = team2_points
        result2["Verlorene Ballpunkte"] = team1_points
        results.append(result2)

    df = pd.DataFrame(results).groupby("Mannschaft").sum()
    df['Ballpunkteverhältnis'] = df['Gewonnene Ballpunkte'] / (df['Gewonnene Ballpunkte'] + df['Verlorene Ballpunkte'])
    df['Satzverhältnis'] = df['Gewonnene Sätze'] / (df['Gewonnene Sätze'] + df['Verlorene Sätze'])
    df = df.sort_values(by=["Punkte", "Satzverhältnis", "Ballpunkteverhältnis"], ascending=False)
    df["Platz"] = range(1, len(df) + 1)
    return df
