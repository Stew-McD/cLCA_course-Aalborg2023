#%% 

from import_csv import write_database
from LCA_calculations import get_LCA_scores
#from make_process_diagram import make_process_diagram

import bw2data as bd
import bw2io as bi
import bw2calc as bc

#%%
# bd.projects.set_current('cLCA-aalborg')
# bd.databases

bio = bd.Database("biosphere3")

models = ["bread", "corn"]

for model in models:
    try:
        del bd.databases["fg_"+model]
    except:
        pass

bd.databases

# for db in bd.databases:
#     db = bd.Database(db)
#     print(db)
#     print(db.metadata)

for model in models:
    write_database(model)
    # get_LCA_scores(model)
    # make_process_diagram(model)


# %%
