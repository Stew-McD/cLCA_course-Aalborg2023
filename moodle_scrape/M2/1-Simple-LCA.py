#!/usr/bin/env python
# coding: utf-8

# # 1. Simple LCA in Brightway2

# The most important data structures of brightway are represented [here](https://1.docs.brightway.dev/_images/org-scheme.png) and described [here](https://2.docs.brightway.dev/intro.html). Look at the figure  and try to make the parallel with what you know already (e.g. Simapro). I recommend that later you read carefully this documentation page. This is also the terminology to use when working with Brightway2.

# We again use the example product system from Heijungs & Suh (2002)
# 
# The point with tis script is to understand the dict structure of a brightway database.

# In[7]:


import brightway2 as bw # start with "bw." to use a function from the brightway2 module


# In[8]:


bw.projects.set_current('advlca23') # bw.projects.output_dir to find out where projects are stored in the hd


# In[9]:


#bw.databases.clear() # line to use in case you had already databases in the project space
bw.databases # lists all databases. We start from an empty project


# In[10]:


# This cell is to clean up
#del bw.databases['testdb'] 
#del bw.databases['testbiosphere']


# In[11]:


t_db = bw.Database("testdb") # creates an instance of the database class # t_db.name for example.


# In[12]:


# This is the most important cell in this notebook, read it carefully
t_db.write({
    ("testdb", "Electricity production"):{ # Note that a tuple is used to identify an activity univocally
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'liters',
                'type': 'technosphere'
            },{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Electricity production'), #important to write the same process name in output
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            }]
        },
    ('testdb', 'Fuel production'):{ # here starts another activity
        'name': 'Fuel production',
        'unit': 'liters',
        'exchanges':[{
                'input': ('testdb', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Crude oil'),
                'amount': -50,
                'unit': 'liters',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'liters',
                'type': 'production'
            }]
    },
    ('testdb', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'}, # env exchanges
    ('testdb', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testdb', 'Crude oil'):{'name': 'Crude oil', 'unit':'liters', 'type': 'biosphere'}

    })


# In[13]:


bw.databases # Now I see the database


# Now solve the inventory

# In[14]:


functional_unit = {t_db.get("Electricity production") : 1000}
lca = bw.LCA(functional_unit) 
lca.lci()
print(lca.inventory) # Is this what you expected?


# We can't do the LCIA because we have no characterisation factors yet. So we create a LCIA method.

# In[15]:


lca.supply_array


# In[16]:


myLCIAdata = [[('testdb', 'Carbon dioxide'), 1.0], 
              [('testdb', 'Sulphur dioxide'), 2.0],
              [('testdb', 'Crude oil'), 0.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = bw.Method(method_key)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()


# In[17]:


lca = bw.LCA(functional_unit, method_key) # run LCA calculations again with method
lca.lci()
lca.lcia()
lca.score

print("characterized_inventory\n", lca.characterized_inventory)
print("Score\n", lca.score) # same as in the previous script


# Why 'score'? The point with 'score' is that what in Brightway2 is called a "method" is in fact an "impact category"...
# So all characterised results of the method are correctly summed up.

# In[18]:


import numpy as np
np.sum(lca.characterized_inventory) == lca.score


# # Same but different

# Here a different way to link the technosphere and biosphere flows. 
# This time we create two databases, "testdb"  for product flows and 'testbiosphere' for environmental flows (This is closer to how brightway works with commercial dabases such as ecoinvent). 
# 
# Note how the two are linked. Before you had this input line in "testdb":
# 
# ```python
# 'input': ('testdb', 'Carbon dioxide')
# ```
# now you have this one instead:
# 
# ```python
# 'input': ('testbiosphere', 'Carbon dioxide')
# ```
# 
# Run the script and check that you get the same results as before.  

# In[19]:


if 'testdb' in bw.databases: del bw.databases['testdb'] # just another way to clean up
if 'testbiosphere' in bw.databases: del bw.databases['testbiosphere'] # just another way to clean up
bw.databases


# In[20]:


bs_db = bw.Database("testbiosphere")

bs_db.write({
    ('testbiosphere', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testbiosphere', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('testbiosphere', 'Crude oil'):{'name': 'Crude oil', 'unit':'liters', 'type': 'biosphere'}
    })


# In[21]:


t_db = bw.Database("testdb")

t_db.write({
    ("testdb", "Electricity production"):{
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('testdb', 'Fuel production'),
                'amount': 2,
                'unit': 'liters',
                'type': 'technosphere'
            },{
                'input': ('testbiosphere', 'Carbon dioxide'), # the KEY line, this exchange is from the "testbsiosphere" database.
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testbiosphere', 'Sulphur dioxide'),
                'amount': 0.1,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Electricity production'), 
                'amount': 10,
                'unit': 'kWh',
                'type': 'production'
            }]
        },
    ('testdb', 'Fuel production'):{
        'name': 'Fuel production',
        'unit': 'liters',
        'exchanges':[{
                'input': ('testbiosphere', 'Carbon dioxide'),
                'amount': 10,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testbiosphere', 'Sulphur dioxide'),
                'amount': 2,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testbiosphere', 'Crude oil'),
                'amount': -50,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('testdb', 'Fuel production'),
                'amount': 100,
                'unit': 'liters',
                'type': 'production'
            }]
    }}) # Differnetly from before, I don't have the environmental exchanges here


# In[22]:


bw.databases # Now I see also the testbiosphere one


# In[23]:


# I need a new LCIA meethod too!
myLCIAdata = [[('testbiosphere', 'Carbon dioxide'), 1.0], # testbiosphere instead of testdb
              [('testbiosphere', 'Sulphur dioxide'), 2.0],
              [('testbiosphere', 'Crude oil'), 0.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = bw.Method(method_key)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()


# In[24]:


functional_unit = {t_db.get("Electricity production") : 1000}
lca = bw.LCA(functional_unit, method_key) #run LCA calculations again with method
lca.lci()
lca.lcia()
print(lca.score)


# # Exercise in group

# Model the product system in the "Heat production exercise" slides using first excel then brighway2 and make sure you get the same result.
# (Practical hint: when you do the brightway2 version make a copy of this notebook and edit that direclty)

# # Exercise (optional, at home)

# Take your own product system, select two or three activities that are linked together, and that have also some environmental exchanges associated with, and make by hand a database using the Brightway2 standard dict structure. Run the calculations on that. If you don't have data, use the data [here](http://moutreach.science/2017/12/01/LCI-reporting.html#fnref:2).

# # A note on co-products
# There are at least two ways to model co-products with the substitution method. Besides the exchange types `‘technosphere’`, `‘biosphere’`, and `‘production’` there is a fourth type called `‘substitution’`. You can use that (use __plus__ sign!). See the [docs about exchanges](https://2.docs.brightway.dev/intro.html#exchanges). Alternatively, you can simply create an exchange of the `‘technosphere’` type but using the __minus__ sign. I.e. a negative input of some product. This is similar to e.g. SimaPro where there are two options: either use the predefined line for co-products or insert a negative input from technosphere.
# 
# The signs issue is explained very clearly in the [introduction docs](https://2.docs.brightway.dev/intro.html) under “Getting the signs right”. Note that this is perfectly consistent with the Hejiungs and Suh (2002) book chapter. Diagonal values in the A matrix are positive, off-diagonal inputs are negative. Intervention matrix signs depend on the convention (you decide the sign or you have to follow the convention used of the database, e.g. the database may assume that +10 kg CO2 means the emission of CO2 and +10 kg crude oil means the extraction of oil). 
# 
# To use the __partitioning method__ one needs to calculate the allocated values (by mass/energy/revenue etc) for each exchange before importing the data into Brightway2 (or write a code that does that automatically), just like in e.g. SimaPro. 
