import streamlit as st
from game_loader import read_game_data
from game_processor import preprocess
from simulator import run_simulation
from visualizer import plot_matrix
from stqdm import stqdm
from logger import logger
import pandas as pd

logger.debug("Start app")

# Set the title and page icon
st.set_page_config(page_title="Volleyball Tabellensimulation", page_icon="🏐")

st.title("Volleyball Tabellensimulation")

# Create two columns
col1, col2 = st.columns([2, 1])

url = col1.text_input("URL mit Spielplan")

# Slider for selecting a value between 10 and 1000
sim_count = col2.slider("Anzahl Simulationen:", value=10, min_value=1, max_value=1000, step=10)

# Submit button

if st.button("Simuliere"):
    df = read_game_data(url)
    if df.empty:
        st.warning('Kein gültiger Spielplan unter der URL. (z.B. https://www.hessen-volley.de/servlet/league/PlayingScheduleCsvExport?matchSeriesId=70123325)')
    else:
        df_past, df_future, df_team_point_statistics = preprocess(df)

        simulations = list()
        for counter in stqdm(range(sim_count)):
            simulation = run_simulation(df_past, df_future, df_team_point_statistics)
            logger.debug(f'Simulation: {simulation}')
            simulations.append(simulation)

        ranking_expectations = pd.DataFrame(simulations)
        # sort ranking expectations by mean
        ranking_expectations = ranking_expectations[ranking_expectations.mean().sort_values().index]

        rank_statistics = ranking_expectations.describe()
        logger.debug(f"Ranking statistics: \n{rank_statistics}")
        # Count how often each rank was achieved
        rank_counts = ranking_expectations.apply(pd.Series.value_counts).fillna(0)
        logger.debug(f"Rank count: \n{rank_counts}")

        # Plot the ranking expectations
        st.pyplot(plot_matrix(ranking_expectations, sim_count))

        logger.debug("Simulation finished")

# Footer with a website link
st.markdown("2025 [Nicolai Erbs](https://www.erbs.eu) ([Impressum](http://erbs.eu/impressum/))")