#!/usr/bin/env python
# coding: utf-8

# # 4. Import data from MS Excel

# Brightway2 has a series of options for data import and export that you are invited to read about and try, they are on the official website and notebook. 
# 
# However, you can also developed your own importer, that fits with your workflow. For example, the file `lci_to_bw2.py` includes a code to convert a properly formatted csv file into a Brightway2 database dict. You need to install the Python Data Analysis Library [pandas](https://pandas.pydata.org/) to make it work (within your virtual environment, run `conda install pandas` or `pip install pandas` if you are not using conda). 
# 
# How does this importer work? 
# 
# 1. Prepare your inventory in MS Excel using the template. See the example file _test\_db\_excel\_w\_ecoinvent.xlsx_
# 2. Save the relevant MS Excel sheet as .csv file, see the example file _test\_db\_excel\_w\_ecoinvent.csv_
# 3. Import the module in your script with the command `from lci_to_bw2 import *` 
# 4. Import the .csv file as a dataframe with the pandas function `.read_csv()`. Clean it up for unnecessary columns.
# 5. Convert the dataframe into a dict using the function `lci_to_bw2()`
# 6. Save the dict as a Brightway2 database in the usual way i.e. using Brightway's `Database()`and `.write()` functions.
# 
# **NOTE:** this importer contains no automated tests so you need to make sure manually that the excel and csv files are in good order.
# 
# See an example below.

# In[1]:


import pandas as pd
import numpy as np
import brightway2 as bw
from lci_to_bw2 import * # import all the functions of this module


# In[7]:


mydb = pd.read_csv('test_db_excel_w_ecoinvent.csv', header = 0, sep = ",") # using csv file avoids encoding problem
mydb.head()


# In[8]:


# clean up a bit
mydb = mydb.drop('Notes', 1)  # remove the columns not needed
mydb['Exchange uncertainty type'] = mydb['Exchange uncertainty type'].fillna(0).astype(int) # uncertainty as integers
# Note: to avoid having both nan and values in the uncertainty column I use zero as default
mydb.head()


# In[9]:


# Create a dict that can be written as database
bw2_db = lci_to_bw2(mydb) # a function from the lci_to_bw2 module
bw2_db


# In[10]:


bw.projects.set_current('advlca23') # Find a project where there is ecoinvent 3.9 conseq
bw.databases


# Time to write the data on a database. 
# 
# Important: 
# 
# - The database **name should be the same** as in the excel file...
# 
# - make sure you **shut down** all other notebooks using **the same bw project** before you run this. Only one user at the time can write on a database. Otherwise you'll get a "Database locked" error.

# In[11]:


t_db = bw.Database('exldb') # it works because the database name in the excel file is the same
# shut down all other notebooks using the same project
t_db.write(bw2_db)


# In[12]:


bw.databases # It worked


# Give a look at your imported database

# In[13]:


[print(act) for act in t_db]  # check more stuff 
print('---------')
[[print(act, exc) for exc in list(act.exchanges())]for act in t_db]  # check more stuff 
print('---------')
[[print(exc.uncertainty) for exc in list(act.exchanges())]for act in t_db]  # check more stuff


# In[14]:


myact = bw.Database("exldb").get('Fuel production')
list(myact.exchanges())


# Let's check if calculations work

# In[16]:


mymethod = ('IPCC 2013', 'climate change', 'global warming potential (GWP100)')
el = t_db.get("Electricity production")
functional_unit = {el: 1000}
lca = bw.LCA(functional_unit, mymethod)
lca.lci()
lca.lcia()
print(lca.score)


# # Question
# Do you think this results includes all emissions you have imported from the excel file?

# # Group exercise 
# 
# ### (This is for the portfolio you don't need to do it now, we'll start it during the online lecture) 
# Prepare your own product system in excel, linked to biosphere3 and ecoinvent, and import it. Run calculations to see if it works as expected. Send all the code and data to another group and see if they can reproduce your results, in that case, the exercise will be a success. Get feedback from other group on your code and what difficulties they had in reading and running it.
