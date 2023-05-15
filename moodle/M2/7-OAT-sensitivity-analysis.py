#!/usr/bin/env python
# coding: utf-8

# # One At the Time (OAT) Sensitivity analysis

# This is the simplest case. Also called a _local_ Sensitivity analysis. One parameter is changed by keeping all the other constant and the difference in results is compared to the change. This allows to investigate how much results are affected by the specific change in the parameter. This is good for some types of analysis, but has some problems. Main issue is that the effect of a change in the parameter might be different when other parameters assume different values...so OAT can be misleading!  This problem can only be solved with a global sensitivity analysis (next notebook)

# In[1]:


import brightway2 as bw
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# In[2]:


bw.projects.set_current('advlca23') # Still working in the same project
bw.databases


# In[3]:


#if 'sa_db' in bw.databases: del bw.databases['sa_db'] # to clean up if you do this multiple times
#bw.databases


# In[3]:


SA_db = bw.Database('sa_db')

# A simplified db, one foreground activity: 'Electricity production,
# linked to a background one: 'market for electricity, low voltage' (kilowatt hour, DK, None)
SA_db.write({  
    ('sa_db', 'el_prod_for_sa'): {
        'name': 'Electricity production',
        'unit': 'kilowatt hour',
        'exchanges': [{
            'input': ('ecoinvent 3.9 conseq', 'ce40dd006e462e720eb669efbc31dd59'), # Danish market for electricity
            'amount': 1,
            'type': 'technosphere'},
        {
            'input': ('sa_db', 'el_prod_for_sa'),
            'amount': 1,
            'type': 'production'}]}})

# select the foreground activity and calculate result
lca = bw.LCA({SA_db.get('el_prod_for_sa'): 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
lca.lci()
lca.lcia()
DK_result = lca.score
DK_result


# # Changing the exchange kind
# 
# There are many ways of doing sensitivity analysis. One might for example be interested in changing the electricity mix (somebody might call this a _scenario analysis_...). For example, I would like to run my LCA with ten different market mixes in ecoinvent instead of just the Danish one.

# In[4]:


# First make a list of processes we wants to change with, in this case el. markets
el_markets = [('ecoinvent 3.9 conseq', i['code']) 
              for i in bw.Database("ecoinvent 3.9 conseq").search('market electricity low voltage', limit = 100)]
el_markets[1:5] # prints the first four of them


# In[5]:


# Make a copy of the activity, substitute the background process, save and calculate
SA_el_loc_results = [] # empty list that will contain all the results of the local SA
el = SA_db.get('el_prod_for_sa')
for m in el_markets[0:20]: # I am just taking the first 20 of them to speed up
    el2 = el.copy() # implement the changes on a copy to keep the original intact
    exc = list(el2.exchanges())[0] # select the first exchange in the activity, i.e. the input from ecoinvent
    exc['input'] = m
    exc.save() # important or the changes won't be maintained
    lca = bw.LCA({el2: 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
    lca.lci()
    lca.lcia()
    SA_el_loc_results.append(lca.score)


# In[6]:


SA_el_loc_results


# In[8]:


# Unig numpy and pandas packages here
print(np.mean([(i/DK_result) for i in SA_el_loc_results])) # about 7 times higher impact than DK on average
pd.DataFrame(SA_el_loc_results).describe()


# In[9]:


# Using matplotlib package
plt.boxplot(SA_el_loc_results)
plt.ylabel(bw.methods[('IPCC 2013', 'climate change', 'global warming potential (GWP100)')]['unit'])
plt.xlabel('El Production')


# # Changing the exchange value
# 
# One might want to test different values for the same exchange, or see how results are affected by a percent change in the value of this exchange. Iin this case it's more handy to use _parametrized inventories_. There is a good [tutorial here](https://nbviewer.jupyter.org/urls/bitbucket.org/cmutel/brightway2/raw/default/notebooks/Parameters%20-%20manual%20creation.ipynb) about this that you can check it out, as well as some [theory here](https://docs.brightwaylca.org/intro.html#parameterized-datasets) on what type of parameters (activity-, database-, or project-parameters) one can define in brightway. Here we make just a simple example. 

# ## Without parameters

# In[10]:


list(SA_db.get('el_prod_for_sa').exchanges())[0]


# In[11]:


# the obvious solution is to use the same approach as above
SA_values = [1.01, 1.05, 1.1] # I am studying a change of 1%, 5%, 10% in the parameter
SA_el_value_results = []
el = SA_db.get('el_prod_for_sa')
for v in SA_values:
    el2 = el.copy()
    exc = list(el2.exchanges())[0]
    exc['amount'] = v # this is the different line compared to before
    exc.save()
    lca = bw.LCA({el2: 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
    lca.lci()
    lca.lcia()
    SA_el_value_results.append(lca.score)


# In[12]:


SA_el_value_results


# In[13]:


plt.plot(SA_values, SA_el_value_results)
plt.ylabel('SA results')
plt.xlabel('SA values')


# In[14]:


(SA_el_value_results[0] - DK_result)/(1.01 - 1.) # Marginal change (slope of the line)


# In[15]:


from scipy import stats # just another way to do the same
slope, intercept, r_value, p_value, std_err = stats.linregress(SA_values, SA_el_value_results)
slope, intercept, r_value, p_value, std_err


# ## Same but using parameters

# In[16]:


print(bw.parameters) # you shuold have none


# In[17]:


# If you get a result like: "Parameters manager with 1 objects" then comment out and run this cell
#from bw2data.parameters import *

#for param in ActivityParameter.select(): 
#    print(param, param.amount) # This is to check what aprameters are in your notebook already

#del bw.databases['sa_db'] # delete the database to clean up existing Database and activity parameters
#bw.parameters.remove_from_group("my group", bw.Database('sa_db').get('el_prod_for_sa')) # also a way to clean up 


# In[18]:


get_ipython().run_line_magic('pinfo2', 'bw.parameters')


# In[17]:


# Same product system as before but including a parameter
SA_db = bw.Database('sa_db')
SA_db.write({  
    ('sa_db', 'el_prod_for_sa'): {
        'name': 'Electricity production',
        'unit': 'kilowatt hour',
        'exchanges': [{
            'input': ('ecoinvent 3.9 conseq', 'ce40dd006e462e720eb669efbc31dd59'), 
            'amount': 1.0,
            'type': 'technosphere',
            'formula': 'my_parameter'}, # I added a new line here with the parameter "my_parameter"
        {
            'input': ('sa_db', 'el_prod_for_sa'),
            'amount': 1.0,
            'type': 'production'}]}})


# In[18]:


# Define the details of the parameter 'my_parameter'
activity_data = [ {
    'name': 'my_parameter',
    'amount': 1.0,
    'database': 'sa_db',
    'code' : 'somecode'
}]


# In[19]:


bw.parameters # still nothing


# In[20]:


# First register these parameters
from bw2data.parameters import *
parameters.new_activity_parameters(activity_data, "my group", overwrite=True) # add a group name for the parameters

for param in ActivityParameter.select():
    print(param, param.amount)


# Parameter Activation is in **two steps**

# In[21]:


# 1) Need to declare which activities have exchanges with parameters
parameters.add_exchanges_to_group("my group", SA_db.get('el_prod_for_sa'))

# 2) Update the exchanges with the new parameter value
ActivityParameter.recalculate_exchanges("my group")

# check if it worked
for exc in SA_db.get('el_prod_for_sa').exchanges():
    print(exc.amount, exc.input, exc.output)


# In[22]:


# This is how you change the value of a parameter
ActivityParameter.update(amount = 2.0).where(ActivityParameter.name == 'my_parameter').execute()

# Need to do this as well if you want to see the new value of the exchange (otherwise only the parameter changes)
ActivityParameter.recalculate_exchanges("my group")

# check if it worked
for exc in SA_db.get('el_prod_for_sa').exchanges():
    print(exc.amount, exc.input, exc.output)


# In[35]:


# Now this can be done in a loop for a series of values
SA_values = [1.01, 1.05, 1.1]
SA_el_value_results = []
for v in SA_values:
    ActivityParameter.update(amount = v).where(ActivityParameter.name == 'my_parameter').execute() # key line
    ActivityParameter.recalculate_exchanges("my group")
    for exc in SA_db.get('el_prod_for_sa').exchanges():
        print(exc.amount, exc.input, exc.output)
    lca = bw.LCA({SA_db.get('el_prod_for_sa') : 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
    lca.lci()
    lca.lcia()
    SA_el_value_results.append(lca.score)


# In[36]:


SA_values


# In[37]:


SA_el_value_results


# In[38]:


from matplotlib import pyplot as plt
plt.plot(SA_values, SA_el_value_results)
plt.ylabel('SA results')
plt.xlabel('SA values')


# One advantage of using parameters is that a parameter can be applied in multiple places in an inventory

# In[39]:


SA_db = bw.Database('sa_db')
SA_db.write({  
    ('sa_db', 'el_prod_for_sa'): {
        'name': 'Electricity production',
        'unit': 'kilowatt hour',
        'exchanges': [{
            'input': ('ecoinvent 3.9 conseq', 'ce40dd006e462e720eb669efbc31dd59'),  # Danish el market
            'amount': 0.5,
            'type': 'technosphere',
            'formula': 'my_parameter'}, # one parameter here 
        { 
            'input': ('ecoinvent 3.9 conseq', 'e8583fe3173b312b6d6a1bb6e9da5c49'), # German el market
            'amount': 0.5,
            'type': 'technosphere',
            'formula': 'my_parameter'}, # the same parameter is also here
        {
            'input': ('sa_db', 'el_prod_for_sa'),
            'amount': 1,
            'type': 'production'}]}})


# In[40]:


lca = bw.LCA({SA_db.get('el_prod_for_sa') : 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
lca.lci()
lca.lcia()
print(lca.score)


# In[41]:


from bw2data.parameters import *

# define and register parameter
activity_data = [{
    'name': 'my_parameter',
    'amount': 1,
    'database': 'sa_db',
    'code' : 'somecode'}]

parameters.new_activity_parameters(activity_data, "my group", overwrite=True)

# activate parameter
parameters.add_exchanges_to_group("my group", SA_db.get('el_prod_for_sa')) # 1 step
ActivityParameter.recalculate_exchanges("my group") # 2 step

# Check if it worked
for param in ActivityParameter.select():
    print(param, param.amount)
for exc in SA_db.get('el_prod_for_sa').exchanges():
    print(exc.amount, exc.input, exc.output)


# In[42]:


# Same loop as before, this time the parameter changes in two places
SA_values = [0.5, 0.5*1.1, 0.5*0.9] # a change of plus/minus 10%
SA_el_value_results = []
for v in SA_values:
    ActivityParameter.update(amount = v).where(ActivityParameter.name == 'my_parameter').execute()
    ActivityParameter.recalculate_exchanges("my group")
    lca = bw.LCA({SA_db.get('el_prod_for_sa') : 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
    lca.lci()
    lca.lcia()
    SA_el_value_results.append(lca.score)
SA_el_value_results


# In[43]:


plus1 = ( SA_el_value_results[1] - SA_el_value_results[0] ) / SA_el_value_results[0]  
minus1 = ( SA_el_value_results[2] - SA_el_value_results[0] ) / SA_el_value_results[0]
plus1, minus1


# In[44]:


plus1 + minus1 # not exactly zero. Why?


# In[45]:


plt.plot(SA_values, SA_el_value_results, 'bo')
plt.ylabel('SA results')
plt.xlabel('SA values')

