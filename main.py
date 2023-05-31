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
# Set up models
models = []
models.append("bread") 
models.append('corn')

# set to True if you want to run that function
remove = False
rebuild = True
# Load the packages we will need
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
recalculate = True
recalculate_MC = True
revisualise = True

# Remove old results folder
if remove == True and os.path.exists('results'):
    shutil.rmtree('results')

# set parameters for Monte Carlo analysis
iterations = 10000
scale_percent = 0.3
dist_id = 3 # normal - 2 is lognormal 
mc_type = ""
if dist_id == 3: mc_type = "Normal_"+str(iterations)
elif dist_id == 2: mc_type = "Lognormal_"+str(iterations)


# set scenarios for testing sensitivity

scenarios = {
    "CoproductsToWaste": False,
    "EnergyEfficient": False,
    "WaterEfficient": False,
    "CoproductsToLowerMarket": True,
}
#%%
# Write databases from csv files, add uncertainties, inspect and export, make process diagrams
if rebuild == True:
    for model in models:
        write_database(model)
        add_uncertainties(model, dist_id, scale_percent) # see ids below
        inspect_db(model)
        export_db(model)

        if redo_diagrams == True:
            nodes, edges, model = extract_nodes_edges(model)
            write_process_diagram(nodes, edges, model)

fg = bd.Database(f'fg_{model}')


#%% Set up scenarios

for model in models:
    scenario_name = ""
    for k, v in scenarios.items():
        if v == True:
            if k == 'LessSubsitution':
                print("\n***************** Scenario: {} *****************\n".format(k))
                act = bd.get_node(name=f'Purification ({model})')
                if model == 'bread': waste = bd.get_node(code='e343521ccabc453ec59738b1d5678118') # 'treatment of biowaste, industrial composting'
                if model == 'corn': waste = bd.get_node(code='6e199e3cc577ca27b046f0a9898192c2') # 'treatment of inert waste, sanitary landfill'
                edge = [x for x in list(act.technosphere()) if x['amount'] < 0]
                print(f"Changed co-products destination from market to waste: {edge} --> {waste}")
                edge[0]['amount'] *= -1
                edge[0]['input'] = ('con391', waste['code'])
                edge[0].save()
                scenario_name = f'{k}'
            if k == 'CoproductsToWaste':
                print("\n***************** Scenario: {} *****************\n".format(k))
                act = bd.get_node(name=f'Purification ({model})')
                if model == 'bread': waste = bd.get_node(code='e343521ccabc453ec59738b1d5678118') # 'treatment of biowaste, industrial composting'
                if model == 'corn': waste = bd.get_node(code='6e199e3cc577ca27b046f0a9898192c2') # 'treatment of inert waste, sanitary landfill'
                edge = [x for x in list(act.technosphere()) if x['amount'] < 0]
                print(f"Changed co-products destination from market to waste: {edge} --> {waste}")
                edge[0]['amount'] *= -1
                edge[0]['input'] = ('con391', waste['code'])
                edge[0].save()
                scenario_name = f'{k}'

            if k == 'CoproductsToLowerMarket':
                print("\n***************** Scenario: {} *****************\n".format(k))
                act = bd.get_node(name=f'Purification ({model})')
                if model == 'bread': waste = bd.get_node(code='16b7ce830141a933f9537e199cbd608e') # 'treatment of biowaste, industrial composting'
                # if model == 'corn': waste = bd.get_node(code='6e199e3cc577ca27b046f0a9898192c2') # 'treatment of inert waste, sanitary landfill' 
                edge = [x for x in list(act.technosphere()) if x['amount'] < 0]
                print(f"Changed co-products destination from market to waste: {edge} --> {waste}")
                edge[0]['amount'] *= -1
                edge[0]['input'] = ('con391', waste['code'])
                edge[0].save()
                scenario_name = f'{k}'

            if k == 'EnergyEfficient':
                print("\n***************** Scenario: {} *****************\n".format(k))
                for act in fg:
                    for edge in list(act.technosphere()):
                        input = bd.get_node(code=edge.as_dict()['input'][1])
                        name = input['name']
                        if 'electricity' in name: 
                            print(name) 
                            amount1 = edge['amount']
                            edge['amount'] *= 0.5
                            edge.save()
                            amount2 = edge['amount']
                            print(f"Changed edge amount from {amount1} to {amount2} for \n{edge}")
                            scenario_name = f'{k}'

            if k == 'WaterEfficient':
                print("\n***************** Scenario: {} *****************\n".format(k))
                for act in fg:
                    for edge in list(act.technosphere()):
                        input = bd.get_node(code=edge.as_dict()['input'][1])
                        name = input['name']
                        if 'water' in name: 
                            print(name) 
                            amount1 = edge['amount']
                            edge['amount'] *= 0.5
                            edge.save()
                            amount2 = edge['amount']
                            print(f"Changed edge amount from {amount1} to {amount2} for \n{edge}")
                            scenario_name = f'{k}'

            else:
                print("No scenario selected")

    nodes, edges, model = extract_nodes_edges(model)
    write_process_diagram(nodes, edges, model, scenario_name)

#%%
if recalculate == True:
    for model in models:
        lca = get_LCA_scores(model, scenario_name)
        get_LCA_report(model, scenario_name)

#%% Calculate Monte Carlo results
if recalculate_MC == True:
    for model in models:
        single_score = get_LCA_scores(model, scenario_name)
        get_MCLCA_scores(model, single_score, iterations, mc_type, scenario_name)
#%% Plot Monte Carlo results and do statistical tests
import cowsay 
if revisualise == True:
    df = vis.plot_MC_results(mc_type, scenario_name)
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

