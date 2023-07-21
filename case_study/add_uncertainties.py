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
def add_uncertainties(model, dist_id=3, scale_percent=0.1):
    fg = bd.Database("fg_"+ model)
    for node in fg:
        for edge in node.exchanges():
            edge['uncertainty type'] = dist_id #NormalUncertainty.id
            edge['loc'] = (edge['amount'])
            edge['scale'] = round_to_sf(abs(edge['loc']*scale_percent), 6) 

            if dist_id == 2: 
                edge['scale'] = np.log(1 + scale_percent/10)
                edge['loc'] = np.log(abs(edge['amount']))
            if edge['amount'] < 0: edge['negative'] = "True"
            else: edge['negative'] = "False"
            if edge['amount'] == 0: edge['uncertainty type'] = 1
            if edge['amount'] == 0: edge['loc'] = 0 # NoUncertainty.id
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
"""
STATS_ARRAYS DISTRIBUTION IDS
 0: stats_arrays.distributions.undefined.UndefinedUncertainty,
 1: stats_arrays.distributions.undefined.NoUncertainty,
 2: stats_arrays.distributions.lognormal.LognormalUncertainty,
 3: stats_arrays.distributions.normal.NormalUncertainty,
 4: stats_arrays.distributions.geometric.UniformUncertainty,
 5: stats_arrays.distributions.geometric.TriangularUncertainty,
 6: stats_arrays.distributions.bernoulli.BernoulliUncertainty,
 7: stats_arrays.distributions.discrete_uniform.DiscreteUniform,
 8: stats_arrays.distributions.weibull.WeibullUncertainty,
 9: stats_arrays.distributions.gamma.GammaUncertainty,
 10: stats_arrays.distributions.beta.BetaUncertainty,
 11: stats_arrays.distributions.extreme.GeneralizedExtremeValueUncertainty,
 12: stats_arrays.distributions.student.StudentsTUncertaint
"""