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

# # Working with the OECD - ICIO database

# The OECD Inter-Country Input-Output tables (ICIO) are available on the [OECD webpage.](https://www.oecd.org/sti/ind/inter-country-input-output-tables.htm) 
#
# The parsing function >parse_oecd< works for both, the 2016 and 2018 release.

# The tables can either be downloaded manually (using the csv format), or the pymrio [OECD automatic downloader can be used](autodownload.ipynb#OECD-download).

# For example, to get the 2011 table of the 2018 release do:

import pymrio

from pathlib import Path

oecd_storage = Path('/tmp/mrios/OECD')

meta_2018_download = pymrio.download_oecd(storage_folder=oecd_storage, years=[2011])

# OECD provides the data compressed in zip files. The pymrio oecd parser works with both, the compressed and unpacked version.

# ## Parsing

# To parse a single year of the database, either specify a path and year:

oecd_path_year = pymrio.parse_oecd(path=oecd_storage, year=2011)

# Or directly specify a file to parse:

oecd_file = pymrio.parse_oecd(path=oecd_storage / 'ICIO2018_2011.zip')

oecd_path_year == oecd_file

# Note: The original OECD ICIO tables provide some disaggregation of the Mexican and Chinese tables for the interindustry flows. The pymrio parser automatically aggregates these into Chinese And Mexican totals. Thus, the MX1, MX2, .. and CN1, CN2, ... entries are aggregated into MEX and CHN.

# Currently, the parser only includes the value added and taxes data given in original file as satellite accounts.
# These are accessable in the extension "factor_inputs":

oecd_file.factor_inputs.F.head()

# Handling of the data happens similar to the other databases, see for example ["Exploring EXIOBASE"](working_with_exiobase.ipynb#Exploring-EXIOBASE).
