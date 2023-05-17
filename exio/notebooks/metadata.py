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

# # Metadata and change recording

# Each pymrio core system object contains a field 'meta' which stores meta data as well as changes to the MRIO system. This data is stored as json file in the root of a saved MRIO data and accessible through the attribute '.meta':

import pymrio
io = pymrio.load_test()

io.meta

io.meta('Loaded the pymrio test sytem')

# We can now do several steps to modify the system, for example:

io.calc_all()
io.aggregate(region_agg = 'global')

io.meta

# Notes can added at any time:

io.meta.note('First round of calculations finished')

io.meta

# In addition, all file io operations are recorde in the meta data:

io.save_all('/tmp/foo')

io_new = pymrio.load_all('/tmp/foo')

io_new.meta

# The top level meta data can be changed as well. These changes will also be recorded in the history:

io_new.meta.change_meta('Version', 'v2')

io_new.meta

# To get the full history list, use:

io_new.meta.history

# This can be restricted to one of the history types by:

io_new.meta.modification_history

# or

io_new.meta.note_history
