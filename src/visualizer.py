import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot_matrix(expectations, num_simulations):
    # Count the number of each rank for each team
    expectations = expectations.apply(pd.Series.value_counts).fillna(0).astype(int)
    # Convert the count to a percentage
    expectations = expectations / num_simulations * 100.0
    print(expectations)
    
    # Plot the ranking expectations as a heatmap with the team names on the x axis and the count of each rank on the y axis
    plt.figure(figsize=(10, 6))
    ax = sns.heatmap(expectations, annot=True, fmt=".1f", cmap="Greens", cbar=False)


    for t in ax.texts:
        if t.get_text() == "0.0":
            t.set_text("")
        else:
            t.set_text(t.get_text() + " %")

    plt.xticks(rotation=45)
    plt.title(f"Erwartete Platzierungen ({num_simulations} Simulationen)")
    plt.xlabel("Team")
    plt.ylabel("Platzierung")
    plt.subplots_adjust(bottom=0.25)

    return plt