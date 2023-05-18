#%% 

from import_db_from_file import write_database
from add_uncertainties import add_uncertainties
from LCA_calculations import get_LCA_scores, get_MCLCA_scores
import visualisation as vis
#from make_process_diagram import make_process_diagram

import bw2data as bd
import bw2io as bi
import bw2calc as bc
import os
import shutil

#%% 
bd.projects.set_current('cLCA-aalborg')

remove = True
if remove == True and os.path.exists('results'):
    shutil.rmtree('results')


models = ["corn"] 
models += ['bread']

for model in models:
    write_database(model)
    add_uncertainties(model)

bd.databases
#%% 
for model in models:
    get_LCA_scores(model)
    # make_process_diagram(model)

# %%
for model in models:
    get_MCLCA_scores(model, iterations=10000)

vis.plot_MC_results()
# %%
