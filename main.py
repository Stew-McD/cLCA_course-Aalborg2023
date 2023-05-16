#%% 

from import_csv import write_database
# from LCA_calculations import get_LCA_scores
# from make_process_diagram import make_process_diagram

import bw2data as bd
import bw2io as bi
import bw2calc as bc

#%%
bd.projects.set_current('cLCA-aalborg')
bd.databases

models = ['bread', 'corn']

for model in models:
    write_database(model)
    #get_LCA_scores(model)
    #make_process_diagram(model)

bd.databases

ei = bd.Database('con391')
bio = bd.Database('biosphere3')
bio.random().as_dict()

for db in bd.databases:
    print(db, "\n", bd.Database(db).metadata, "\n")

bd.get_node(code='4ec70203-13b0-58cc-b4dd-2fcce8a96732')
a = bd.get_node(code='Succinic acid production (corn)')
b = bd.get_node(code='Succinic acid production (bread)')
a.as_dict()
list(a.technosphere())
b.as_dict()
list(b.technosphere())