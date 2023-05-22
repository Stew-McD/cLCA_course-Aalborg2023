#%% 

import os
import sys
import shutil

import bw2calc as bc
import bw2data as bd
import bw2io as bi

bi.__version__
bd.__version__
bc.__version__

import seaborn as sns

import visualisation as vis
from add_uncertainties import add_uncertainties
from import_db_from_file import write_database, inspect_db, export_db
from LCA_calculations import get_LCA_scores, get_MCLCA_scores, get_LCA_report
from make_process_diagram import extract_nodes_edges, write_process_diagram

#%%

#%% 
bd.projects.set_current('cLCA-aalborg')

# set to True if you want to run that function
remove = False
rebuild = True
recalculate = True
recalculate_MC = True
revisualise = True


# Remove old results folder
if remove == True and os.path.exists('results'):
    shutil.rmtree('results')

# Set up models
models = []
models.append("bread") 
models.append('corn')

if rebuild == True:
    for model in models:
        write_database(model)
        add_uncertainties(model, dist_id=3, scale_percent=0.2) # see ids below
        inspect_db(model)
        export_db(model)

for model in models: 
    nodes, edges, model = extract_nodes_edges(model)
    write_process_diagram(nodes, edges, model)

#%%
if recalculate == True:
    for model in models:
        lca = get_LCA_scores(model)
        get_LCA_report(model)
        print(lca.score)
        print(lca.method)

#%% Calculate Monte Carlo results
if recalculate_MC == True:
    for model in models:
        single_score = get_LCA_scores(model)
        get_MCLCA_scores(model, single_score, iterations=100)
#%% Plot Monte Carlo results and do statistical tests
import cowsay 
if revisualise == True:
    df = vis.plot_MC_results(distribution_type='Normal_100')
    dic = df.describe().to_dict()

    results_list = []
    results_list.append("==== Results for Monte Carlo analysis ====")
    for key in dic.keys():
        results_list.append("\n***  "  + key + "kg CO2eq / kg  ***")
        for k, v in dic[key].items():
            results_list.append(f"{k}, {v}")
        print(cowsay.turtle('\n'.join(results_list)))
 
    # with open('results/MC_results_cowsay.txt', 'w') as f:
    #     f.write(x)

#%%

# import bw2analyzer as ba
# from bw2analyzer import ContributionAnalysis 
# ContributionAnalysis().annotated_top_processes(lca)
# ContributionAnalysis().annotated_top_emissions(lca)

# lca.dicts.X.biosphere
# ContributionAnalysis().d3_treemap(lca.dict
                                 
# import bw2calc as bc
# from bw2calc import graph_traversal as gt

# lca.demand
# act = bd.get_node(id=lca.demand.keys[0])

# bc.utils.print_recursive_supply_chain(lca.activity)
# gt.AssumedDiagonalGraphTraversal().calculate(lca)
# gt.MultifunctionalGraphTraversal().calculate(lca)


# """
# STATS_ARRAYS DISTRIBUTION IDS
#  0: stats_arrays.distributions.undefined.UndefinedUncertainty,
#  1: stats_arrays.distributions.undefined.NoUncertainty,
#  2: stats_arrays.distributions.lognormal.LognormalUncertainty,
#  3: stats_arrays.distributions.normal.NormalUncertainty,
#  4: stats_arrays.distributions.geometric.UniformUncertainty,
#  5: stats_arrays.distributions.geometric.TriangularUncertainty,
#  6: stats_arrays.distributions.bernoulli.BernoulliUncertainty,
#  7: stats_arrays.distributions.discrete_uniform.DiscreteUniform,
#  8: stats_arrays.distributions.weibull.WeibullUncertainty,
#  9: stats_arrays.distributions.gamma.GammaUncertainty,
#  10: stats_arrays.distributions.beta.BetaUncertainty,
#  11: stats_arrays.distributions.extreme.GeneralizedExtremeValueUncertainty,
#  12: stats_arrays.distributions.student.StudentsTUncertaint
# """
