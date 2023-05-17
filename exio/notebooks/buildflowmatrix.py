# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Analysing the source of stressors (flow matrix)

# To calculate the source (in terms of regions and sectors) of a certain stressor or impact driven by consumption, one needs to diagonalize this stressor/impact. This section shows how to do this based on the 
# small test mrio included in pymrio. The same procedure can be use for any other MRIO, but keep in mind that
# diagonalizing a stressor dramatically increases the memory need for the calculations.

# ## Basic example

# First we load the test mrio:

import pymrio
io = pymrio.load_test()

# The test mrio includes several extensions:

list(io.get_extensions())

# For the example here, we use 'emissions' - 'emission_type1':

io.emissions.F

et1_diag = io.emissions.diag_stressor(('emission_type1', 'air'), name = 'emtype1_diag')

# The parameter name is optional, if not given the name is set to the stressor name + '_diag'

# The new emission matrix now looks like this:

et1_diag.F.head(15)

# And can be connected back to the system with:

io.et1_diag = et1_diag

# Finally we can calulate the all stressor accounts with:

io.calc_all()

# This results in a square footprint matrix. In this matrix, every column respresents the amount of stressor occuring in each region - sector driven by the consumption stated in the column header. Conversly, each row states where the stressor impacts occuring in the row are distributed due (from where they are driven).

io.et1_diag.D_cba.head(20)

# The total footprints of a region - sector are given by summing the footprints along rows:

io.et1_diag.D_cba.sum(axis=0).reg1

io.emissions.D_cba.reg1

# The total stressor in a sector corresponds to the sum of the columns:

io.et1_diag.D_cba.sum(axis=1).reg1

io.emissions.F.reg1

# ## Aggregation of source footprints

# If only one specific aspect of the source is of interest for the analysis, the footprint matrix can easily be aggregated with the standard pandas groupby function. 
#
# For example, to aggregate to the source region of stressor, do:

io.et1_diag.D_cba.groupby(level='region', axis=0).sum()

# In addition, the [aggregation function](../notebooks/aggregation_examples.ipynb) of pymrio also work on the diagonalized footprints. Here as example together with the [country converter coco](https://github.com/IndEcol/country_converter):

import country_converter as coco
io.aggregate(region_agg = coco.agg_conc(original_countries=io.get_regions(), 
                                        aggregates={'reg1': 'World Region A',
                                                    'reg2': 'World Region A',
                                                    'reg3': 'World Region A',},
                                         missing_countries='World Region B'))

io.et1_diag.D_cba
