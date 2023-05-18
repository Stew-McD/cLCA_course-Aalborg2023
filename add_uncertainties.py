#%%

import bw2data as bd
import bw2calc as bc

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stats_arrays import NormalUncertainty, LognormalUncertainty

# function for rounding numbers to significant figures

def round_to_sf(num, significant):
    if num == 0:
        return 0
    # Calculate the exponent to determine the number of significant figures
    exponent = math.floor(math.log10(abs(num))) + 1
    # Calculate the multiplier to obtain the desired significant figures
    multiplier = 10 ** (significant - exponent)
    # Round the number and divide by the multiplier to obtain the rounded value
    rounded_num = round(num * multiplier) / multiplier

    return rounded_num

#%%
# bd.projects.set_current("cLCA-aalborg")
# model = "bread"
def add_uncertainties(model):
    fg = bd.Database("fg_"+ model)
    for node in fg:
        for edge in node.exchanges():
            edge['uncertainty type'] = NormalUncertainty.id
            edge['loc'] = abs(edge['amount'])
            edge['scale'] = round_to_sf(abs(edge['loc']*0.05), 6) # 20% uncertainty
            if edge['amount'] <= 0: edge['negative'] = True
            else: edge['negative'] = False
            edge.save()

# scales = []
# for node in fg:
#     for edge in node.exchanges():
#         e = edge.as_dict()
#         print(e["amount"], " : ", e["scale"])
#         # plt.hist(edge.random_sample(n=1000))
#         scales.append(e["amount"])

# scales = pd.Series(scales)
# scales.describe()
# # edge.random_sample(10)


# %%
