from logger import logger


def ranking(games_df):
    logger.debug("Calculating ranking")
    # Calculate the sum of all Ballpunkte columns for each player
    ranking = games_df.filter(like="Ballpunkte").sum(axis=1)
    # Sort the players by their total Ballpunkte
    ranking = ranking.sort_values(ascending=False)
    return ranking


def divide_games(df):
    #Divide the games into two dataframes based on whether the row contains values in the colum "Satzpunkte" and "Ballpunkte"
    logger.debug("Dividing games")
    df_past = df.loc[df["Satzpunkte"].notnull()]
    df_future = df.loc[df["Satzpunkte"].isnull()]
    return df_past, df_future


def extract_result(df):
    # Extract the result from the column "Satzpunkte" and "Ballpunkte" and create the columns ["Satzpunkte1", "Satzpunkte2", "Ballpunkte1", "Ballpunkte2"]
    logger.debug("Extracting result")
    df = df.copy()
    df["Satzpunkte1"] = df["Satzpunkte"].str.split(":").str[0].astype(int)
    df["Satzpunkte2"] = df["Satzpunkte"].str.split(":").str[1].astype(int)
    df["Ballpunkte1"] = df["Ballpunkte"].str.split(":").str[0].astype(int)
    df["Ballpunkte2"] = df["Ballpunkte"].str.split(":").str[1].astype(int)
    return df
    

def remove_invalid_games(df):
    # Remove all rows where the value of any column containing Ballpunkte is 0
    logger.debug("Removing invalid games")
    return df.loc[(df.loc[:, df.columns.str.contains("Ballpunkte")] != 0).all(axis=1)]
