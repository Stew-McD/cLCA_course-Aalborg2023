#%% USE THIS FILE TO RUN THE LCA CALCULATION

#%% Import the necessary packages

import bw2data as bd
import bw2calc as bc
import seaborn as sb

import bw_processing as bwp
import matrix_utils as mu
import bw2calc as bc
import numpy as np
import seaborn as sb
import pandas as pd

import os
#%% Set the project
bd.projects.set_current('cLCA-aalborg')
if not os.path.exists('results'): os.makedirs('results')

# look for the activity in the database

def get_LCA_scores(model):    #%% Set the functional unit for the LCA calculation
    print("\n***************** LCA calculations *****************\n")
    
    db_name = "fg_"+model
    fg = bd.Database(db_name)
    fg.search('Succinic')
    fu = {'name' : 'Succinic acid production ({})'.format(model), 'amount': 1}
    # find it in the database
    myact = fg.get(fu['name'])
    ID = myact.id
    
    # another way to do it, looking at all databases in the project
    myact2 = bd.get_node(name=fu['name'])
    # check that they are the same
    myact2 == myact

    # look at the exchanges of the functional unit
    print("The functional unit is: \n{}, with an amount of {} {}".format(myact['name'], fu['amount'], myact['unit']))
    exchanges = list(myact.exchanges())
    print("\n*****\nThe exchanges of the functional unit are: \n")
    print(*exchanges, sep = "\n")


#Define the method for the LCA calculation
    # list all the methods available
    method_list = list(bd.methods)

# eg. 
# ('CML v4.8 2016 no LT',
# 'acidification no LT',
# 'acidification (incl. fate, average Europe total, A&B) no LT')

    # choose one
    # method_search_string = 'material'
    # method_search = [x for x in method_list if method_search_string in " ".join(x).lower()]
    #print(method_search)

    # you can also do it like this
    mymethod = ('IPCC 2013', 'climate change', 'global warming potential (GWP100)')
    # mymethod_object = bd.Method(mymethod)

    #%% Run the LCA calculation
    lca = bc.LCA(
        demand = {myact : fu['amount']},
        method = mymethod,
        use_distributions = False)
    lca.lci()
    lca.lcia()

    #%% print the results
    print(("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is: {} {}".format(myact.as_dict()['name'], fu['amount'], myact.as_dict()['unit'], lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit'])))
    if not os.path.exists('results'): os.makedirs('results')

# write results to a file
    with open('results/LCA_results.txt', 'a+') as f:
        f.write(("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is: {} {}".format(myact.as_dict()['name'], fu['amount'], myact.as_dict()['unit'], lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit'])))

    # %% Monte Carlo LCA calculations
def get_MCLCA_scores(model, iterations=100):
    print("\n***************** Monte carlo - LCA calculations *****************\n")
    
    db_name = "fg_"+model
    fg = bd.Database(db_name)
    fu = {'name' : 'Succinic acid production ({})'.format(model), 'amount': 1, 'unit': 'kg'}
    mymethod = ('IPCC 2013', 'climate change', 'global warming potential (GWP100)')
    myact = fg.get(fu['name'])
 
    lca = bc.LCA(
        demand = {myact : fu['amount']},
        method = mymethod,
        use_distributions = True)
    
    lca.lci()
    lca.lcia()

    mc_results = [lca.score for _ in zip(range(iterations), lca)]
    mc_res = pd.DataFrame(mc_results, columns=[mymethod[2]]).sort_values(ascending=False, by = mymethod[2])
    mc_res['MC iteration'] = mc_res.index.to_series()

    mc_res.describe()
    
    fig = mc_res.plot(kind='scatter', x='MC iteration', y=mymethod[2], title='Monte Carlo results for Succinic acid production ({})'.format(model), logy=False)

    fig.figure.savefig('figures/MC_LCA_{}.png'.format(model))
    #%% print the results
    print("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is ({}):\n {}".format(myact.as_dict()['name'], fu['amount'], myact.as_dict()['unit'], lca.method, bd.Method(mymethod).metadata['unit'], mc_res[mymethod[2]].describe()))

# write results to a file
    if not os.path.exists('results'): os.makedirs('results')
    with open('results/MC_LCA_results.txt', 'a') as f:
        f.write(("\n\n*****************\n\t For the FU: '{}' {} {} \n\t with the method '{}' \n\tthe LCIA score is: {} {}".format(myact.as_dict()['name'], fu['amount'], myact.as_dict()['unit'], lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit'])))

# write results to a csv file, appending a new column for each model
#%%
    try:
        df = pd.read_csv('results/MC_LCA_results.csv')
    except:
        df = pd.DataFrame()

    df[model+" @ "+mymethod[2]] = mc_res[mymethod[2]]
    df.to_csv('results/MC_LCA_results.csv', header=True, index=False)

