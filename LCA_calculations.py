#%% USE THIS FILE TO RUN THE LCA CALCULATION

#%% Import the necessary packages

import bw2data as bd
import bw2calc as bc

#%% load the project and define the databases

#%% 
# # list all the projects
# list(bd.projects)

# # open the project in brightway2
# bd.projects.set_current('cLCA-aalborg')

# # list the databases in the project
# list(bd.databases)

# #  Define the databases
# ei = bd.Database('con391')
# bio = bd.Database('biosphere3')
# fg = bd.Database('fg_csv')

# # look for the activity in the database
# fg.search('Succinic')

def get_LCA_scores(model):    #%% Set the functional unit for the LCA calculation
    print("\n***************** LCA calculations *****************\n")
    
    db_name = "fg_"+model
    fg = bd.Database(db_name)
    fu = {'name' : 'Succinic acid production ({})'.format(model), 'amount': 1, 'unit': 'kg'}
    # find it in the database
    myact = fg.get(fu['name'])
    # another way to do it, looking at all databases in the project
    # myact2 = bd.get_node(name=fu['name'])
    # check that they are the same
    # myact2 == myact

    # look at the exchanges of the functional unit
    # print("The functional unit is: \n{}, with an amount of {} {}".format(myact['name'], fu['amount'], myact['unit']))
    # exchanges = list(myact.exchanges())
    # print("*****\nThe exchanges of the functional unit are: \n")
    # print(*exchanges, sep = "\n\n")


#Define the method for the LCA calculation
    # list all the methods available
    # method_list = list(bd.methods)


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
    # set to FU for the 
    functional_unit = {bd.get_node(name=fu['name']): fu['amount']}
    lca = bc.LCA(functional_unit, mymethod)
    lca.lci()
    lca.lcia()

    #%% print the results
    print("*****************\n\t For the FU: '{}' \n\t with the method '{}' \n\t the LCIA score is: {}".format(functional_unit, lca.method, round(lca.score, 2)), bd.Method(mymethod).metadata['unit'])

# write results to a file

    with open('LCA_results.txt', 'a') as f:
        f.write("*****************\n\t For the FU: '{}' \n\t with the method '{}' \n\t, the LCIA score is: {}".format(functional_unit, lca.method, round(lca.score, 2), bd.Method(mymethod).metadata['unit']))

    # %%