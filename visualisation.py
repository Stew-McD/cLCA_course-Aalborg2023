#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from stats_arrays import uncertainty_choices
import os

import palettable.wesanderson as wa


#%%# Read the CSV file into a DataFrame
def plot_MC_results(distribution_type='Normal_1000'):
    """Plot results of Monte Carlo analysis for Succinic acid production"""
    # Read the CSV file into a DataFrame
    directory = 'results'
    csv_files = [f for f in os.listdir(directory) if f.endswith(distribution_type+'.csv')]
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    csv_file = csv_files[0]
    csv_path = os.path.join(directory, csv_file)
    results_df = pd.read_csv(csv_path)

    # get uncertainty type and iterations from the csv file name
    dist_type = csv_file.split('_')[-2]

    # clear the plot from previous runs
    # plt.clf()
    # plt.cla()

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

        # Calculate the y-coordinate for the annotation based on the limits of the y-axis
    ymin, ymax = ax.get_ylim()
    y = ymin + 0.1 * (ymax - ymin)

    for col in results_df.columns:

                # Add text to the plot
        mean = results_df[col].mean()
        std = results_df[col].std()
        min = results_df[col].min()
        max = results_df[col].max()
        single_score = col.split('@')[2]

        plt.annotate(f'Single score: {single_score}\nMean: {mean:.2f}\nStd: {std:.2f}\nMin: {min:.2f}\nMax: {max:.2f}',
                xy=(mean, y),
                ha='center',
                va='center',
                color='black', 
                fontsize=10,
                path_effects=[path_effects.withStroke(linewidth=3, foreground='white')],
                bbox=dict(edgecolor='black', boxstyle='round', facecolor='white', alpha=0.1),
        )
    
    # Do a statistical test to see if the two distributions are significantly different
        # look here for information https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/

    from scipy.stats import ttest_ind, mannwhitneyu, ks_2samp

    # welch's t-test
    stat_WT, p_WT = ttest_ind(results_df.iloc[:,0], results_df.iloc[:,1], equal_var=False)
    print('t =', stat_WT)
    print(f'p = {p_WT:.2e}')
    

    # Mann-Whitney U test
    stat_MW, p_MW = mannwhitneyu(results_df.iloc[:,0], results_df.iloc[:,1])
    print('stat_MW =', stat_MW)
    print(f'p_PS = {p_MW:.2e}')

    # Kolmogorov-Smirnov test
    stat_KS, p_KS = ks_2samp(results_df.iloc[:,0], results_df.iloc[:,1])
    print('stat_KS =', stat_KS)
    print(f'p_KS = {p_KS:.2e}')



    # Add a legend to the plot and some other information
    plt.legend(fontsize=20)
    plt.ylabel('Distribution Density', fontsize=14)
    plt.xlabel(f"{results_df.columns[0].split('@')[1].title()} (kg CO$_2$(eq)/kg FU)", fontsize=14)
    plt.title('Monte Carlo LCIA results for Succinic acid production scenarios', fontsize=24)
    plt.annotate("Number of iterations: {}\nUncertainty type: {}".format(len(results_df), dist_type), xy=(0.5, 0.95), fontsize = 16, xycoords='axes fraction', ha='center', va='center', bbox=dict(edgecolor='black', boxstyle='round', facecolor='white', alpha=0.1))

    # add statistical test results to the plot
    plt.annotate("Welch's t-test\nstat = {:.2f}\np = {:.2e}".format(stat_WT, p_WT), xy=(0.05, 0.95), xycoords='axes fraction', ha='left', va='center', bbox=dict(edgecolor='black', boxstyle='round', facecolor='white', alpha=0.1))
    plt.annotate("Mann-Whitney U test\nstat = {:.2f}\np = {:.2e}".format(stat_MW, p_MW), xy=(0.05, 0.85), xycoords='axes fraction', ha='left', va='center', bbox=dict(edgecolor='black', boxstyle='round', facecolor='white', alpha=0.1))
    plt.annotate("Kolmogorov-Smirnov test\nstat = {:.2f}\np = {:.2e}".format(stat_KS, p_KS), xy=(0.05, 0.75), xycoords='axes fraction', ha='left', va='center', bbox=dict(edgecolor='black', boxstyle='round', facecolor='white', alpha=0.1))

    # print statistical tests results to the console
    print("*** Welch's t-test\nstat = {:.2f}\np = {:.2e}".format(stat_WT, p_WT))
    print("*** Mann-Whitney U test\nstat = {:.2f}\np = {:.2e}".format(stat_MW, p_MW))
    print("*** Kolmogorov-Smirnov test\nstat = {:.2f}\np = {:.2e}".format(stat_KS, p_KS))

    # print statistical tests results to a text file
    with open('figures/MC_LCA_results_statistics_{}_{}.txt'.format(dist_type, len(results_df)), 'w') as f:
        f.write("*** Welch's t-test\nstat = {:.2f}\np = {:.2e}\n".format(stat_WT, p_WT))
        f.write("*** Mann-Whitney U test\nstat = {:.2f}\np = {:.2e}\n".format(stat_MW, p_MW))
        f.write("*** Kolmogorov-Smirnov test\nstat = {:.2f}\np = {:.2e}\n".format(stat_KS, p_KS))


    #ax.set_xlim(min(results_df.min()), max(results_df.max()))
    # Show the plot
    plt.show()
    fig.tight_layout()
    fig
    # Save the plot
    fig.savefig('figures/MC_LCA_results_distplot_{}_{}.svg'.format(dist_type, len(results_df)))
    plt.close()

    return results_df
    
# %%

if __name__ == "__main__":
    plot_MC_results()