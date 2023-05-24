# %% USE THIS FILE TO RUN THE LCA CALCULATION

# %% Import the necessary packages

import bw2data as bd
import bw2calc as bc
import seaborn as sb

import bw2analyzer as ba
from bw2analyzer import ContributionAnalysis as ca

import bw_processing as bwp
import matrix_utils as mu
import bw2calc as bc
import numpy as np
import seaborn as sb
import pandas as pd


import os
from stats_arrays import uncertainty_choices
# %% Set the project
bd.projects.set_current('cLCA-aalborg')
if not os.path.exists('results'):
    os.makedirs('results')


def get_LCA_report(model):

    db_name = "fg_"+model
    fg = bd.Database(db_name)
    fu = {'name': 'Succinic acid production ({})'.format(model), 'amount': 1}
    # find it in the database
    myact = fg.get(fu['name'])

    mymethod = ('IPCC 2013', 'climate change',
                'global warming potential (GWP100)')

    lca = bc.LCA(
        demand={myact: fu['amount']},
        method=mymethod,
        use_distributions=False)
    lca.lci()
    lca.lcia()

    # from bw2calc import graph_traversal as gtrav

    # # gt = gtrav.AssumedDiagonalGraphTraversal().calculate(lca)
    # # # gt.MultifunctionalGraphTraversal().calculate(lca)

    # # import bw2analyzer as ba
    # # from bw2analyzer import ContributionAnalysis as ca
    # # from bw2analyzer import print_recursive_supply_chain, PageRank, traverse_tagged_databases
    # # from bw2analyzer.econ import gini_coefficient, herfindahl_index, concentration_ratio, theil_index
    # # income = lca.characterized_inventory.data
    # # gini_coefficient(income), herfindahl_index(income), concentration_ratio(income), theil_index(income)

    with open("results/recursive_calculation_{}.csv".format(model), "w") as f:
        ba.print_recursive_calculation(
            myact, mymethod, max_level=10, file_obj=f, tab_character=";", cutoff=0.05)

    with open("results/recursive_supply_chain_{}.csv".format(model), "w") as f:
        ba.print_recursive_supply_chain(
            myact, max_level=10, file_obj=f, tab_character="    ", cutoff=0.05)

    with open("results/top_emissions_{}.csv".format(model), "w") as f:
        top_emissions = ca().annotated_top_emissions(lca)
        header = "LCIA score; Inventory amount; Biosphere flow"
        f.write("{}\n".format(header))
        for e in top_emissions:
            f.write(f"{e[0]};{e[1]};{e[2]}\n")

    with open("results/top_processes_{}.csv".format(model), "w") as f:
        top_processes = ca().annotated_top_processes(lca)
        header = "LCIA score; Supply amount; Activity"
        f.write("{}\n".format(header))
        for e in top_processes:
            f.write(f"{e[0]}; {e[1]}; {e[2]}\n")

    # %% print the results
    print(("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is: {} {}".format(myact.as_dict()
          ['name'], fu['amount'], myact.as_dict()['unit'], lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit'])))
    if not os.path.exists('results'):
        os.makedirs('results')

# write results to a file
    with open('results/LCA_results.txt', 'a+') as f:
        f.write(("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is: {} {}".format(myact.as_dict()
                ['name'], fu['amount'], myact.as_dict()['unit'], lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit'])))

    print("reports written to file")


def get_LCA_scores(model):  # %% Set the functional unit for the LCA calculation
    print("\n***************** LCA calculations *****************\n")

    db_name = "fg_"+model
    fg = bd.Database(db_name)
    fg.search('Succinic')
    fu = {'name': 'Succinic acid production ({})'.format(model), 'amount': 1}
    # find it in the database
    myact = fg.get(fu['name'])
    ID = myact.id

    # another way to do it, looking at all databases in the project
    myact2 = bd.get_node(name=fu['name'])
    # check that they are the same
    myact2 == myact

    # look at the exchanges of the functional unit
    print("The functional unit is: \n{}, with an amount of {} {}".format(
        myact['name'], fu['amount'], myact['unit']))
    exchanges = list(myact.exchanges())
    print("\n*****\nThe exchanges of the functional unit are: \n")
    print(*exchanges, sep="\n")


# Define the method for the LCA calculation
    # list all the methods available
    method_list = list(bd.methods)

# eg.
# ('CML v4.8 2016 no LT',
# 'acidification no LT',
# 'acidification (incl. fate, average Europe total, A&B) no LT')

    # choose one
    # method_search_string = 'material'
    # method_search = [x for x in method_list if method_search_string in " ".join(x).lower()]
    # print(method_search)

    # you can also do it like this
    mymethod = ('IPCC 2013', 'climate change',
                'global warming potential (GWP100)')
    # mymethod_object = bd.Method(mymethod)

    # %% Run the LCA calculation
    lca = bc.LCA(
        demand={myact: fu['amount']},
        method=mymethod,
        use_distributions=False)
    lca.lci()
    lca.lcia()

    # %% print the results
    print(("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is: {} {}".format(myact.as_dict()
          ['name'], fu['amount'], myact.as_dict()['unit'], lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit'])))
    if not os.path.exists('results'):
        os.makedirs('results')

# write results to a file
    with open('results/LCA_results.txt', 'a+') as f:
        f.write(("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is: {} {}".format(myact.as_dict()
                ['name'], fu['amount'], myact.as_dict()['unit'], lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit'])))

    return lca

    # %% Monte Carlo LCA calculations


def get_MCLCA_scores(model, single_score, iterations, mc_type):
    print("\n***************** Monte carlo - LCA calculations *****************\n")

    db_name = "fg_"+model
    fg = bd.Database(db_name)
    fu = {'name': 'Succinic acid production ({})'.format(
        model), 'amount': 1, 'unit': 'kg'}
    mymethod = ('IPCC 2013', 'climate change',
                'global warming potential (GWP100)')
    myact = fg.get(fu['name'])

    lca = bc.LCA(
        demand={myact: fu['amount']},
        method=mymethod,
        use_distributions=True)

    lca.lci()
    lca.lcia()

    mc_results = [lca.score for _ in zip(range(iterations), lca)]
    mc_res = pd.DataFrame(mc_results, columns=[mymethod[2]]).sort_values(
        ascending=False, by=mymethod[2])
    mc_res['MC iteration'] = mc_res.index.to_series()

    mc_res.describe()

    fig = mc_res.plot(kind='scatter', x='MC iteration',
                      y=mymethod[2], title='Monte Carlo results for Succinic acid production ({})'.format(model), logy=False)

    fig.figure.savefig('figures/MC_LCA_{}_{}.png'.format(model, mc_type))
    # %% print the results
    print("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is ({}):\n {}".format(myact.as_dict()
          ['name'], fu['amount'], myact.as_dict()['unit'], lca.method, bd.Method(mymethod).metadata['unit'], mc_res[mymethod[2]].describe()))

# write results to a file
    if not os.path.exists('results'):
        os.makedirs('results')
    with open('results/MC_LCA_results_{}.txt'.format(mc_type), 'a') as f:
        f.write(("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is: {} {}".format(myact.as_dict()
                ['name'], fu['amount'], myact.as_dict()['unit'], lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit'])))

# write results to a csv file, appending a new column for each model
# %%
    try:
        df = pd.read_csv('results/MC_LCA_results_{}.csv'.format(mc_type))
    except:
        df = pd.DataFrame()

    df[model+" @ "+mymethod[2] + " @ " +
        str(round(single_score.score, 2))] = mc_res[mymethod[2]]
    df.to_csv('results/MC_LCA_results_{}.csv'.format(mc_type),
              header=True, index=False)
