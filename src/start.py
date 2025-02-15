from logger import logger
import game_loader, game_processor, team_processor, simulator
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

num_simulations = 100


def run_simulation(df_past, df_future, df_team_point_statistics):
    # Simulate future games
    df_future = simulator.simulate_future_games(df_future, df_team_point_statistics)
    logger.debug(f"{len(df_future.index)} simulated games")
    # Combine past and future games
    df_all = pd.concat([df_past, df_future])

    # Get future ranking
    df_future_team_statistics = team_processor.team_statistics(df_all)
    logger.debug(f"Future ranking: \n{df_future_team_statistics.head(100)}")
    return df_future_team_statistics['Platz'].to_dict()


def plot(expectations):
    # Convert to long format for Seaborn
    long_df = expectations.melt(var_name="Team", value_name="Platzierung")

    
    # Plot the distribution
    plt.figure(figsize=(10, 6))
    ax = sns.violinplot(x="Team", y="Platzierung", data=long_df, inner="quartile", width=1.6)
    plt.gca().invert_yaxis()  # Invert y-axis so rank 1 is at the top
    plt.title("Simulierte Verteilung der Platzierungen")
    plt.xticks([])  # Remove x-axis labels
    plt.yticks(range(1, expectations.columns.size+1))  # Show all ticks from 1 to 10

    plt.xlabel("")  # Remove x-axis label
    
    for i, team in enumerate(expectations.columns):
        ax.text(i, 1, team, ha='center', va='top', rotation=45, fontsize=10)

    plt.show()


def main():
    logger.info("Starting the application")
    df = game_loader.read_game_data_from_file()
    logger.info(f"{len(df.index)} games loaded")
    df_past, df_future = game_processor.divide_games(df)
    logger.info(f"{len(df_past.index)} played games loaded")
    
    df_past = game_processor.extract_result(df_past)

    # Get current ranking
    df_team_statistics = team_processor.team_statistics(df_past)
    logger.info(f"Current ranking: \n{df_team_statistics.head(100)}")
    
    # Compute team statistics
    df_past_filtered = game_processor.remove_invalid_games(df_past)
    logger.info(f"{len(df_past_filtered.index)} played games after filtering")
    df_team_point_statistics = team_processor.team_point_statistics(df_past_filtered)

    simulations = list()
    for i in range(num_simulations):
        simulation = run_simulation(df_past, df_future, df_team_point_statistics)
        logger.info(simulation)
        simulations.append(simulation)

    ranking_expectations = pd.DataFrame(simulations)

    rank_statistics = ranking_expectations.describe()
    logger.info(f"Ranking statistics: \n{rank_statistics}")
    # Count how often each rank was achieved
    rank_counts = ranking_expectations.apply(pd.Series.value_counts).fillna(0)
    logger.info(f"Rank count: \n{rank_counts}")

    # Plot the ranking expectations
    plot(ranking_expectations)

    logger.info("Application finished")


if __name__ == "__main__":
    main()
