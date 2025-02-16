#!/usr/bin/env python
# coding: utf-8

# # 8.1 Modification of a database to run scenarios
# 
# Here we modify the technology matrix without touching the files in the database, this is useful to e.g. modify bacgkround databases like ecoinvent to simulate scenarios and to perform OAT sensitivity analysis relatively fast

# 1. Import BW2, biosphere3 and import ecoinvent database
# 5. modify specific activities in the ecoinvent database (using the technology matrix coordinates)
# 6. calculate results with the modified ecoinvent database

# **Set up**

# In[1]:


import random
import pandas as pd # if you don't have pandas close the notebook and run "conda install pandas" in your virtual env
import numpy as np

# Options for pandas
pd.options.display.max_columns = 50
pd.options.display.max_rows = 50

from scipy.sparse import csr_matrix

import matplotlib.pyplot as plt
import matplotlib as mpl


# In[2]:


import brightway2 as bw


# In[3]:


sorted(bw.projects) # check what project you have 
# bw.projects.delete_project('advlca22', delete_dir=True) # if you want a fresh start


# In[3]:


# Just in case you want a fresh start
# bw.databases.clear()
# bw.methods.clear()


# In[4]:


bw.projects.set_current('advlca23') # Still working in the same project
bw.databases
#bw.databases.clear() # For a fresh start (Risky command! clears all your existing databases)


# # Skip this if you already have biosphere and ecoinvent imported

# In[ ]:


# Import the biosphere3 database
bw.bw2setup()  # This will take some time


# In[ ]:


# Import ecoinvent

ei_vX_dir = "your directory...." # change vX with the version, and change the directory too

if 'ecoinvent X.X.X conseq' in bw.databases: # change X with the version
    print("Database has already been imported")
else:
    ei_vX = bw.SingleOutputEcospold2Importer(ei_vX_dir, 'ecoinvent 3.X.X conseq', use_mp = False) # You can give it another name of course
    ei_vX.apply_strategies()
    ei_vX.statistics()

ei_vX.drop_unlinked(True)
ei_vX.write_database() # This will take some time.


# In[ ]:


bw.databases # you should now see both "biosphere3" and "ecoinvent X.X.X "


# ## Start here if you have already imported the background database

# In[17]:


#frst we find the code of the belgian electircity mix high voltage and we keep it for further use
for activity in bw.Database('ecoinvent 3.9 conseq').search("market for electricity high voltage belgium"):
    print(activity['name'], activity['code'], activity['location'], activity['unit'])


# Now we create a simple foreground process that uses 1 kWh electricity in Belgium

# (Side note: how did I get this code? _a6ce6bd4ed5be000b09a35160a79b673_ 
# 
# I used this link https://www.md5hashgenerator.com/ and typed "Belgian electricity mix" in the text field, then copied the MD5 Hash. This is a way to create unique identifiers for activities)

# In[18]:


fg_db = bw.Database('fg_db') # foreground database
fg_db.write({
    ('fg_db', 'a6ce6bd4ed5be000b09a35160a79b673'):{ # Note that a tuple is used to identify an activity univocally
        'name':'Belgian el mix',
        'unit': 'kilogram', 
        'exchanges': [{
                'input': ('ecoinvent 3.9 conseq', '140f214ea44bf37e5eda0dcf93d055a9'), # 'market for electricity, high voltage' (kilowatt hour, BE, None) found a couple of lines above
                'amount': 1,
                'unit': 'kilowatt hour',
                'type': 'technosphere'
            }]}})
    


# In[20]:


#you can use this to check the inputs of the belgian mix
belgian_mix_default = bw.Database('ecoinvent 3.9 conseq').get('140f214ea44bf37e5eda0dcf93d055a9') # same ei code as before
for exc in belgian_mix_default.exchanges():
    print(exc['type'])
    print(exc['input'][1])
    print(exc.input)
    print(exc['amount'])
    print("-------")


# # Modify the database by changing directly the technology matrix

# Find the products and activities that you need.
# 
# In particular we want to change the shared of wind and gas in the belgian electircity mix

# Initialize the LCA using the FU (this could be the BAU scenario)

# In[22]:


mymethod = ('IPCC 2013', 'climate change', 'global warming potential (GWP100)')
LCA = bw.LCA({('fg_db', 'a6ce6bd4ed5be000b09a35160a79b673') : 1}, 
             mymethod)
LCA.lci()
LCA.lcia()


# In[23]:


LCA.score


# Decide which activities and exchanges to modify. 
# 
# _(You can dedice yourself hot to structure this, below is only a suggestion)_
# 
# I use here a list of **tuples** each tuple with this structure: (activity, exchange, new value) 
# - first element is the column in tech matrix, 
# - second is the row in the tech matrix, 
# - third element of the tuple is the new value (scenario)
# 
# So the first two elements are coordinates and the third is a value

# In[26]:


to_change = [(('ecoinvent 3.9 conseq', '140f214ea44bf37e5eda0dcf93d055a9'), # Belgian el mix
             ('ecoinvent 3.9 conseq', 'ea3613788c223ee88d4c4f176ca4b822'), # wind input to the mix
             0.5), # input increased to 50%
            (('ecoinvent 3.9 conseq', '140f214ea44bf37e5eda0dcf93d055a9'), # Belgian el mix
             ('ecoinvent 3.9 conseq', '1a2d99364e5e44eba30dba550f163677'), #  gas input to the mix
             0.25), # input reduced to 25%
             (("fg_db", "a6ce6bd4ed5be000b09a35160a79b673"), # foreground activity
              ('ecoinvent 3.9 conseq', '140f214ea44bf37e5eda0dcf93d055a9'), # belgian el mix
              1.1)] # input changed 1.1. only for demonstrative purposes

# Belgian el mix == 'market for electricity, high voltage' (kilowatt hour, BE, None)
# wind == 'electricity production, wind, 1-3MW turbine, offshore' (kilowatt hour, BE, None)
# gas == 'electricity production, natural gas, combined cycle power plant' (kilowatt hour, BE, None)


# This is to show the coordinates (column number and row number) in the technology matrix and current values

# In[27]:


for i in to_change:
    col = LCA.activity_dict[i[0]] # the new thing about this notebook is using activity_dict
    row = LCA.activity_dict[i[1]]
    print(col, row, LCA.technosphere_matrix[row,col]) # shows current values


# Using the coordinates of the activities and exchanges to be changed, **update the value**

# In[28]:


for i in to_change:
    col = LCA.activity_dict[i[0]] # find index of tech matrix for the activity
    row = LCA.activity_dict[i[1]] # find index of tech matrix for the exchange
    LCA.technosphere_matrix[row,col] = -i[2] # substitute the value, need to change the sign!
    
    print(col, row, LCA.technosphere_matrix[row,col])


# Now perform calculations using the modified tech matrix

# In[29]:


LCA.redo_lci() # uses the new tech matrix
LCA.lcia()
LCA.score/1.1 # because we have 1.1 times higher input of electricity


# Ths score is diffent as before and lower impact as expected (we have more wind and less gas)

# ### Using data from files (useful to organize scenarios and prepare things on beforehand)

# Same but different, import the scenario from a separate file with the data, that you prepare on beforehand

# In[30]:


scenario_data = pd.read_csv('scenario.csv', sep = ';') # import a csv unsing pandas, careful with formatting...
scenario_data


# Convert the dataframe in a list of tuples

# In[31]:


to_change = []
for i in range(len(scenario_data.index)):
    change = ((scenario_data.iloc[i,0],scenario_data.iloc[i,1]),
              (scenario_data.iloc[i,2],scenario_data.iloc[i,3]),
              scenario_data.iloc[i,4])
    to_change.append(change)


# In[32]:


to_change


# In[16]:


for i in to_change:
    col = LCA.activity_dict[i[0]] # find index of tech matrix for the activity
    row = LCA.activity_dict[i[1]] # find index of tech matrix for the exchange
    LCA.technosphere_matrix[row,col] = -i[2] # substitute the value
    #print(LCA.technosphere_matrix[row,col])


# In[17]:


LCA.redo_lci() # uses the new tech matrix
LCA.lcia()
LCA.score/1.1


# If you have multiple scenarios, you can import each file with a different name and then **iterate the calculation across the scenarios**
