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
ei = bd.Database('con391')

# set to True if you want to run that function
remove = False
rebuild = True
recalculate = True
recalculate_MC = True
revisualise = True

# set parameters
iterations = 1000
scale_percent = 0.3
dist_id = 3
mc_type = ""
if dist_id == 3: mc_type = "Normal_"+str(iterations)
elif dist_id == 2: mc_type = "Lognormal_"+str(iterations)


# set scenarios for testing sensitivity





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
        add_uncertainties(model, dist_id, scale_percent) # see ids below
        inspect_db(model)
        export_db(model)
        nodes, edges, model = extract_nodes_edges(model)
        write_process_diagram(nodes, edges, model)

#%%
if recalculate == True:
    for model in models:
        lca = get_LCA_scores(model)
        get_LCA_report(model)

#%% Calculate Monte Carlo results
if recalculate_MC == True:
    for model in models:
        single_score = get_LCA_scores(model)
        get_MCLCA_scores(model, single_score, iterations,mc_type)
#%% Plot Monte Carlo results and do statistical tests
import cowsay 
if revisualise == True:
    df = vis.plot_MC_results(mc_type)
    dic = df.describe().to_dict()

    results_list = []
    results_list.append("==== Results for Monte Carlo analysis ====")
    for key in dic.keys():
        results_list.append("\n***  "  + key + "kg CO2eq / kg  ***")
        for k, v in dic[key].items():
            results_list.append(f"{k}, {v}")
        print(cowsay.turtle('\n'.join(results_list)))
 


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

