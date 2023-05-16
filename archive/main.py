#%%

import os
import pandas as pd
import numpy as np
import graphviz as gv

import bw2data as bd
import bw2calc as bc


#%% Load the projects and the databases

bd.projects.set_current('cLCA-aalborg')
bd.databases

ei = bd.Database("con391")
bio = bd.Database("biosphere3")
fg = bd.Database("fg_csv")

# %%

for act in fg:
    print(act.as_dict())

# %%
