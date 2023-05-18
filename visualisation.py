import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#%%# Read the CSV file into a DataFrame
def plot_MC_results():
    # Read the CSV file into a DataFrame
    results_df = pd.read_csv('results/MC_LCA_results.csv')

    # Create a distplot of the two Series objects
    for col in results_df.columns:
        sns.distplot(results_df[col], 
        label=col.split('@')[0],)
        mean = results_df[col].mean()
        std = results_df[col].std()
        min = results_df[col].min()
        max = results_df[col].max()
        plt.text(mean, 0.05, f'Mean: {mean:.2f}\nStd: {std:.2f}\nMin: {min:.2f}\nMax: {max:.2f}'
                 , ha='center', va='top',     color='black', fontsize=8)

    # Add a legend to the plot
    plt.legend()
    plt.xlabel(col.split('@')[1])
    plt.title('Monte Carlo results for Succinic acid production')
    plt.annotate("Number of iterations: {}".format(len(results_df)), xy=(0.3, 0.9), xycoords='axes fraction')

    # Show the plot
    plt.show()

    # Save the plot
    plt.savefig('figures/MC_LCA_results_distplot_{}.svg'.format(len(results_df)))
# %%

if __name__ == "__main__":
    plot_MC_results()