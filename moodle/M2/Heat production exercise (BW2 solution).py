#!/usr/bin/env python
# coding: utf-8

# # Heat production exercise (BW2 solution)

# In[1]:


import brightway2 as bw


# In[3]:


bw.projects.set_current('advlca20_heat_exercise') # make a new project


# In[5]:


hx_db = bw.Database("hx") # creates an instance of the database class 'hx' = 'Heat eXercise'


# A suggestion on how to do this in a structured way. Take each **column** of your matrix and create each activity one by one. Make sure you use activity names consistently.

# In[6]:


hx_db.write({
    ("hx", "Coal production"):{
        'name':'Coal from coal production',
        'unit': 'kg', 
        'exchanges': [{
                'input': ('hx', 'Market for electricity'),
                'amount': 0.04,
                'unit': 'kWh',
                'type': 'technosphere'
            },{
                'input': ('hx', 'Carbon dioxide'),
                'amount': 0.34,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('hx', 'Coal production'), 
                'amount': 1.0,
                'unit': 'kg',
                'type': 'production'
            }]
        },
    ("hx", "Power plant"):{
        'name':'Electricity from power plant',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('hx', 'Coal production'),
                'amount': 0.4,
                'unit': 'kg',
                'type': 'technosphere'
            },{
                'input': ('hx', 'Carbon dioxide'),
                'amount': 0.84,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('hx', 'Power plant'), 
                'amount': 1.3,
                'unit': 'kWh',
                'type': 'production'
            }]
        },
    ("hx", "Heat plant"):{
        'name':'Heat from Heat plant',
        'unit': 'MJ', 
        'exchanges': [{
                'input': ('hx', 'Coal production'),
                'amount': -0.4,
                'unit': 'liters',
                'type': 'technosphere'
            },{
                'input': ('hx', 'Carbon dioxide'),
                'amount': 0.84,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('hx', 'Heat plant'),
                'amount': 10.0,
                'unit': 'MJ',
                'type': 'production'
            }]
        },
    ("hx", "Market for electricity"):{
        'name':'Electricity from Market for electricity',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('hx', 'Power plant'), # only UNconstrained activities in the market!
                'amount': 2.6,
                'unit': 'kWh',
                'type': 'technosphere'
            },{
                'input': ('hx', 'Market for electricity'), 
                'amount': 2.6,
                'unit': 'kWh',
                'type': 'production'
            }]
        },
    ("hx", "Market for heat"):{
        'name':'Heat from Market for heat',
        'unit': 'MJ', 
        'exchanges': [{
                'input': ('hx', 'Heat cogeneration'), # only UNconstrained activities in the market!
                'amount': 15,
                'unit': 'MJ',
                'type': 'technosphere'
            },{
                'input': ('hx', 'Market for heat'), 
                'amount': 15,
                'unit': 'MJ',
                'type': 'production'
            }]
        },
    ("hx", "Heat cogeneration"):{
        'name':'Heat from Heat cogeneration',
        'unit': 'MJ', 
        'exchanges': [{
                'input': ('hx', 'Market for electricity'),
                'amount': -1.3,
                'unit': 'kWh',
                'type': 'technosphere' # this is avoided electricity production (the substution method)
            },{
                'input': ('hx', 'Coal production'),
                'amount': 0.4,
                'unit': 'kg',
                'type': 'technosphere'
            },{
                'input': ('hx', 'Carbon dioxide'),
                'amount': 0.84,
                'unit': 'kg',
                'type': 'biosphere'
            },{
                'input': ('hx', 'Heat cogeneration'), 
                'amount': 5,
                'unit': 'MJ',
                'type': 'production'
            }]
        },
    ('hx', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'}

    })


# In[7]:


bw.databases # Now I see the database


# Now solve the inventory

# In[8]:


functional_unit = {hx_db.get("Market for heat") : 10000}
lca = bw.LCA(functional_unit) 
lca.lci()
print(lca.inventory) # you can already see this is close to zero


# In[9]:


import numpy as np # Import the numpy package
np.sum(lca.inventory) # almost zero


# In[10]:


# We don't really need this but let's do it anyway

myLCIAdata = [[('testdb', 'Carbon dioxide'), 1.0]]

method_key = ('simplemethod', 'imaginaryendpoint', 'imaginarymidpoint')
my_method = bw.Method(method_key)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()


# In[11]:


lca = bw.LCA(functional_unit, method_key) # run LCA calculations again with method
lca.lci()
lca.lcia()
lca.score

print("characterized_inventory\n", lca.characterized_inventory)
print("Score\n", lca.score) # The exact result


# In[13]:


lca.supply_array # To see the scaling factors for each activity. 
#Notice that Heat plant is not needed (value = 0) in the system


# ### Note on the substitution method
# 
# In the activity: "Heat cogeneration" you find this:
# 
# ```python
#          'exchanges': [{
#                 'input': ('hx', 'Market for electricity'),
#                 'amount': -1.3,
#                 'unit': 'kWh',
#                 'type': 'technosphere' 
#             },
#             
# ```
# 
# But an **equivalent** way of doing this is using the 'substitution' exchange type with **positive** value:
# 
# ```python
#         'exchanges': [{
#                 'input': ('hx', 'Market for electricity'),
#                 'amount': 1.3, # Positive
#                 'unit': 'kWh',
#                 'type': 'substitution' # different from above
#             },
#             
# ```
# 
