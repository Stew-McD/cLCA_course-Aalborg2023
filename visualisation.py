#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from stats_arrays import uncertainty_choices
import os

import palettable.wesanderson as wa


#%%# Read the CSV file into a DataFrame
def plot_MC_results():
    """Plot results of Monte Carlo analysis for Succinic acid production"""
    # Read the CSV file into a DataFrame
    directory = 'results'
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    csv_file = csv_files[0]
    csv_path = os.path.join(directory, csv_file)
    results_df = pd.read_csv(csv_path)

    # get uncertainty type and iterations from the csv file name
    dist_type = csv_file.split('_')[-2]

    # clear the plot from previous runs
    plt.clf()
    plt.cla()

    # Set the color palette
    colors = wa.GrandBudapest4_5.hex_colors
    sns.set_palette(colors)



    fig, ax = plt.subplots(figsize=(16, 10))
    # Create distplot of the two Series objects
    for col in results_df.columns:
        sns.histplot(data=results_df,
                    x=col,
                    stat='density',
                    kde=True, ax=ax, 
                    label=col.split(' @ ')[0],)
        
        # Add text to the plot
        mean = results_df[col].mean()
        std = results_df[col].std()
        min = results_df[col].min()
        max = results_df[col].max()
        single_score = col.split('@')[2]

        plt.text(mean, ax.get_ylim()[1]*0.05,
                f'Single score: {single_score}\nMean: {mean:.2f}\nStd: {std:.2f}\nMin: {min:.2f}\nMax: {max:.2f}',
                ha='center',
                va='center',
                color='black', 
                fontsize=8,
                path_effects=[path_effects.withStroke(linewidth=3, foreground='white')],
                bbox=dict(edgecolor='black', boxstyle='round', facecolor='white', alpha=0.1),
        )

    # Reset the visual effects back to normal

    # Add a legend to the plot
    plt.legend()
    plt.xlabel(results_df.columns[0].split('@')[1])
    plt.title('Monte Carlo LCIA results for Succinic acid production scenarios')
    plt.annotate("Number of iterations: {}\nUncertainty type: {}".format(len(results_df), dist_type), xy=(0.5, 0.95), xycoords='axes fraction', ha='center', va='center', bbox=dict(edgecolor='black', boxstyle='round', facecolor='white', alpha=0.1))

    #ax.set_xlim(min(results_df.min()), max(results_df.max()))
    # Show the plot
    plt.show()
    fig.tight_layout()
    fig
    # Save the plot
    fig.savefig('figures/MC_LCA_results_distplot_{}_{}.svg'.format(dist_type, len(results_df)))
    plt.close()
    
# %%

if __name__ == "__main__":
    plot_MC_results()