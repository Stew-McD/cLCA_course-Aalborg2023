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

# # Parsing the Eora26 EE MRIO database

# ## Getting Eora26

# The Eora 26 database is available at http://www.worldmrio.com . 
# You need to register there and can then download the files from http://www.worldmrio.com/simplified .

# ## Parse

# To parse a single year do:

import pymrio

eora_storage = '/tmp/mrios/eora26'

# + jupyter={"outputs_hidden": false}
eora = pymrio.parse_eora26(year=2005, path=eora_storage)
# -

# ## Explore

# Eora includes (almost) all countries:

# + jupyter={"outputs_hidden": false}
eora.get_regions()
# -

# This can easily be aggregated to, for example, the OECD/NON_OECD countries with the help of the [country converter coco](https://github.com/IndEcol/country_converter).

import country_converter as coco

# + jupyter={"outputs_hidden": false}
eora.aggregate(region_agg = coco.agg_conc(original_countries='Eora',
                                          aggregates=['OECD'],
                                          missing_countries='NON_OECD')
              )

# + jupyter={"outputs_hidden": false}
eora.get_regions()

# + jupyter={"outputs_hidden": false}
eora.calc_all()

# + jupyter={"outputs_hidden": false}
import matplotlib.pyplot as plt
with plt.style.context('ggplot'):
    eora.Q.plot_account(('Total cropland area', 'Total'), figsize=(8,5))
    plt.show()
# -

# See the other notebooks for further information on [aggregation](../notebooks/aggregation_examples.ipynb) and [file io](../notebooks/load_save_export.ipynb).
