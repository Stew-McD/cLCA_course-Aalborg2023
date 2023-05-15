#!/usr/bin/env python
# coding: utf-8

# # Global Sensitivity Analysis

# This is a more complex case. Involves varying multiple parameters together and understanding which parameter is the one with the largest influence on results. This translates into a large simulation testing the various possibilities. One could use brute force and test all possible combinations of all parameters, and then run a regression on the results where the dependent variable is the impact of the system and the independent variables are the parameters. However, calculating a result for every possible combination might end up taking too much computation time, especially if the number of tested variables is high. Therefore, we use the Saltelli approach and a library called SALib wich is made for this purpose.

# In[1]:


import numpy as np
import scipy as sp
import brightway2 as bw


# In[2]:


bw.projects.set_current('advlca23') # Still working in the same project
bw.databases


# In[3]:


#if 'gsa_db' in bw.databases: del bw.databases['gsa_db'] # to clean up
#bw.databases


# In[4]:


# First make a list of activities, in this case el. markets.
# We want to investigate which of those has the largest influence on the results.

el_markets = [('ecoinvent 3.9 conseq', i['code']) 
              for i in bw.Database("ecoinvent 3.9 conseq").search('market electricity low voltage', limit = 100)]
el_markets[10:15]


# In[5]:


# let's look at what we actually got here
for m in el_markets[10:15]:
    
    elmarket = bw.Database("ecoinvent 3.9 conseq").get(m[1])
    print(elmarket)
    lca = bw.LCA({elmarket: 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
    lca.lci()
    lca.lcia()
    print(lca.score) # The last one is the activity the highest carbon footprint


# In[6]:


# these activities are parameterized into a bw database
gsa_db = bw.Database('gsa_db')
gsa_db.write({  
    ('gsa_db', 'el_prod_for_sa'): {
        'name': 'Electricity production',
        'unit': 'kilowatt hour',
        'exchanges': [{
            'input': ('ecoinvent 3.9 conseq', '33b3d1631b310ce2226ee8ea6166fea9'), 
            'amount': 0.2,
            'type': 'technosphere',
            'formula': 'par0'}, # one parameter here 
        { 
            'input': ('ecoinvent 3.9 conseq', '529c72c85bb0779618357bdc2a365ba1'), 
            'amount': 0.2,
            'type': 'technosphere',
            'formula': 'par1'}, # one parameter here 
        { 
            'input': ('ecoinvent 3.9 conseq', 'e25ef968ab439dbdc0f46ead0f3c2292'), 
            'amount': 0.2,
            'type': 'technosphere',
            'formula': 'par2'}, # one parameter here 
        { 
            'input': ('ecoinvent 3.9 conseq', '8972ca9cadbd942c5daceafacfa52974'), 
            'amount': 0.2,
            'type': 'technosphere',
            'formula': 'par3'}, # one parameter here 
        { 
            'input': ('ecoinvent 3.9 conseq', '5eb3c90350b58ef42a021849b0b9efd2'), 
            'amount': 0.2,
            'type': 'technosphere',
            'formula': 'par4'}, # one parameter here 
        {
            'input': ('gsa_db', 'el_prod_for_sa'),
            'amount': 1.0,
            'type': 'production'}]}})


# We generate a specific sample for our parameters using the Saltelli approach. 
# We will then analyze the results using the Sobol indices.
# For this we need functions from the python library SALib. See [here](https://salib.readthedocs.io/en/stable/getting-started.html) to install SALib with pip and  [here](https://anaconda.org/conda-forge/salib) to install SALib with Conda (remember that you need to install SALib into your BW2 environment! i.e. first activate the environment and then pip/conda install the SALib library)
# 

# In[7]:


from SALib.sample import saltelli
from SALib.analyze import sobol


# In[8]:


from bw2data.parameters import * # we also need the bw parameters


# In[9]:


# Step 1. define parameters and their ranges in form of a problem
problem = { 'num_vars': 5, # number of variables
            'names': ['par0', 'par1', 'par2', 'par3', 'par4'], # names of variables, same as parameters
            'bounds': [[0, 1], [0, 1], # I am going to use percentiles for the first two  
                       [0.2*0.9, 0.2*1.1], [0.2*0.9, 0.2*1.1], # uniform distribution for the other three
                       [0.2*0.9, 0.2*1.1]] } 


# In[10]:


problem


# In[13]:


# Step 2. Generate the samples
param_values = saltelli.sample(problem, 10) # 10 samples only, a very small input space. Returns 120 values.
print(param_values.shape)
param_values[0:5] # This is an array object (package numpy) you can think of it as a grid of values 


# There is a caveaut here. The Saltelli method generates uniform distributions. But let's assume the first two parameters of mine are **not** uniformly distributed. So I convert from percentile to value in the distribution.

# In[14]:


for i in param_values: # for each list of 5 elements...
    i[0] = sp.stats.norm.ppf(i[0], 0.2, 0.01) # normal distribution
    i[1] = sp.stats.lognorm.ppf(i[1], s = 0.1, scale = 0.2) #lognormal, see here:https://stackoverflow.com/questions/8870982/how-do-i-get-a-lognormal-distribution-in-python-with-mu-and-sigma
param_values[0:5]


# If you need to understand the above in more detail

# In[15]:


perc25 = sp.stats.norm.ppf(0.25, 0.2, 0.01) # generate the value of the percentile 0.25  
                                            # of a normal distribution with mean 0.02 and sd 0.01
print(perc25) 


perc50 = sp.stats.norm.ppf(0.5, 0.2, 0.01) # generate the value of the percentile 0.5 (= the mean!!!)  
                                           # of a normal distribution with mean 0.02 and sd 0.01
print(perc50)


# In[16]:


# Step 3. Define the details of each parameter
activity_data = [{'name': 'par0', 'amount': 1.0, 'database': 'gsa_db', 'code' : 'par0code'},
                 {'name': 'par1', 'amount': 1.0, 'database': 'gsa_db', 'code' : 'par1code'},
                 {'name': 'par2', 'amount': 1.0, 'database': 'gsa_db', 'code' : 'par2code'},
                 {'name': 'par3', 'amount': 1.0, 'database': 'gsa_db', 'code' : 'par3code'},
                 {'name': 'par4', 'amount': 1.0, 'database': 'gsa_db', 'code' : 'par4code'}]

parameters.new_activity_parameters(activity_data, "gsagroup", overwrite=True)
parameters.add_exchanges_to_group("gsagroup", gsa_db.get('el_prod_for_sa'))
ActivityParameter.recalculate_exchanges("gsagroup")
for param in ActivityParameter.select():
    print(param, param.amount)


# In[18]:


# Still step 3. Run these samples in our model and store the results in a list. It will take a while
GSA_el_value_results = []
for v in param_values:
    ActivityParameter.update(amount = v[0]).where(ActivityParameter.name == 'par0').execute()
    ActivityParameter.update(amount = v[1]).where(ActivityParameter.name == 'par1').execute()
    ActivityParameter.update(amount = v[2]).where(ActivityParameter.name == 'par2').execute()
    ActivityParameter.update(amount = v[3]).where(ActivityParameter.name == 'par3').execute()
    ActivityParameter.update(amount = v[4]).where(ActivityParameter.name == 'par4').execute()
    
    ActivityParameter.recalculate_exchanges("gsagroup")
    
    lca = bw.LCA({gsa_db.get('el_prod_for_sa') : 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
    lca.lci()
    lca.lcia()
    GSA_el_value_results.append(lca.score)


# In[19]:


# Step 4. Feed the problem and the results to the Sobol function to obtain the Sobol indices 
Si = sobol.analyze(problem, np.array(GSA_el_value_results), print_to_console=True) # must use np.array
# Returns a dictionary with keys 'S1', 'S1_conf', 'ST', and 'ST_conf'
# (first and total-order indices with bootstrap confidence intervals)


# How to interpret this? S1 is the **first-order sensitivity index** (or main effect index), i.e. is the ration between the variance associated with the parameter and the total model variance. It is the *fraction* of total variance that is explained by the parameter. Or, in better words: _it measures the effect of varying the parameter alone, but averaged over variations in other input parameters_ ([See here](https://en.wikipedia.org/wiki/Variance-based_sensitivity_analysis)). In our case _par4_ alone explains alm,ost 50% of the total variance. And seems therefore the most important one - or better, the one to which results are most sensitive to - , followed by _par3_ and _par0_.
# 
# ST instead is the **total-effect index** (or total-order index), i.e. tells how much of the total variance is explained by the parameter taking into account also all its higher order interactions (e.g. the interaciton between _par1_ * _par3_, etc.) Also this case the most important parameter is _par4_ and then secondary parameters are _par0_and _par2_. We now know that _par4_ has not only a large effect but also a large effect in interaction with other parameters.
# 
# However, before we draw some conclusions, let's do two things: first, check the confidence intervals (_conf_ columns) for each index. **They are very large!** So we can't really have much confidence in these results...Second, check the next cell...

# In[20]:


sum(Si['S1']) # Different from 1, so this is not a purely additive model...but is it really true? 
# Or is it just because we didn't have enough simulations?


# # Understanding the Sobol indices even better
# 
# Let's use an even simpler database, increase the number of simulations, and look at the indices again.
# Below here I redo the same but with an even more articifial example, a foreground-only system with only two emissions of equal value. Each of them is parametrised. This ligher system should allow for a faster simulation.
# 
# Since the emissions have equal amount and equal carachterisation factor, we expect that the results will be equally sensitive to each of those. In oher words, these two parameters have equal importance and the sensitivity analysis results should show this.

# In[21]:


t_db = bw.Database('SAtestdb')

t_db.write({
    ("SAtestdb", "Electricity production"):{
        'name':'Electricity production',
        'unit': 'kWh', 
        'exchanges': [{
                'input': ('SAtestdb', 'Carbon dioxide'),
                'amount': 1,
                'unit': 'kg',
                'type': 'biosphere',
                'formula': 'parCO2' # one parameter here
            },{
                'input': ('SAtestdb', 'Sulphur dioxide'),
                'amount': 1, # same value
                'unit': 'kg',
                'type': 'biosphere',
                'formula': 'parSO2' # other parameter here
            },{
                'input': ('SAtestdb', 'Electricity production'), #important to write the same process name in output
                'amount': 1,
                'unit': 'kWh',
                'type': 'production'
            }]
        },
    ('SAtestdb', 'Carbon dioxide'):{'name': 'Carbon dioxide', 'unit':'kg', 'type': 'biosphere'},
    ('SAtestdb', 'Sulphur dioxide'):{'name': 'Sulphur dioxide', 'unit':'kg', 'type': 'biosphere'}
   
    })

myLCIAdata = [[('SAtestdb', 'Carbon dioxide'), 1.0], 
              [('SAtestdb', 'Sulphur dioxide'), 1.0]]

imaginaryLCIAmethod = ('just', 'another', 'LCIAmethod')
my_method = bw.Method(imaginaryLCIAmethod)
my_method.validate(myLCIAdata)
my_method.register() 
my_method.write(myLCIAdata)
my_method.load()


lca = bw.LCA({t_db.get('Electricity production') : 1}, imaginaryLCIAmethod)
lca.lci()
lca.lcia()
print('-----\n-----\n-----\n-----\nlca score =', lca.score)


# In[22]:


# Step 1. define parameters and their ranges in form of a problem
problem = { 'num_vars': 2, 
            'names': ['parCO2', 'parSO2'], 
            'bounds': [[0.9, 1.1], [0.9, 1.1]] }  # 10 % variation

# Step 2. Generate the samples
param_values = saltelli.sample(problem, 1000)
print(param_values.shape)
param_values[0:5]

# Step 3. Define the details of the parameter 'my_parameter'
activity_data2 = [{'name': 'parCO2', 'amount': 1.0, 'database': 'SAtestdb', 'code' : 'parCO2code'},
                 {'name': 'parSO2', 'amount': 1.0, 'database': 'SAtestdb', 'code' : 'parSO2code'}]

parameters.new_activity_parameters(activity_data2, "my group 2", overwrite=True)
parameters.add_exchanges_to_group("my group 2", t_db.get('Electricity production'))
ActivityParameter.recalculate_exchanges("my group 2")
    
GSA_el_value_results = []
for v in param_values:
    ActivityParameter.update(amount = v[0]).where(ActivityParameter.name == 'parCO2').execute()
    ActivityParameter.update(amount = v[1]).where(ActivityParameter.name == 'parSO2').execute()
    
    ActivityParameter.recalculate_exchanges("my group 2")
    
    lca = bw.LCA({t_db.get('Electricity production') : 1}, imaginaryLCIAmethod)
    lca.lci()
    lca.lcia()
    GSA_el_value_results.append(lca.score)

# Step 4. Feed the problem and the results to the Sobol function to obtain the Sobol indices 
Si = sobol.analyze(problem, np.array(GSA_el_value_results), print_to_console=True) # must use np.array
# Returns a dictionary with keys 'S1', 'S1_conf', 'ST', and 'ST_conf'
# (first and total-order indices with bootstrap confidence intervals)


# Easier to interpret. The first order indices have almost the same value. Their error is much lower. The Total effect indices are very close to the first order one. because there is no interaction - and for the same reason the second order indices are close to zero. So everything works as expected and the two parameters are equally important. Moreover...

# In[23]:


sum(Si['S1']) # close to 1, so this confirms it is a purely additive model


# For further understanding on how the Saltelli sampling method works, and how to correctly interpret the Sobol indices, refer to Chapter 4: _Variance based methods_  in Saltelli (2008). Otherwise check the [wikipedia page on variance-based sensitivity analysis](https://en.wikipedia.org/wiki/Variance-based_sensitivity_analysis) which contains a reasonably good summary on Sobol indices and the Saltelli sampling method. 
# 
# _Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., Tarantola, S., 2008. Global Sensitivity Analysis. The Primer, Global Sensitivity Analysis. The Primer. [doi:10.1002/9780470725184](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470725184)_
# 

# # Trying out a different GSA index

# The sobol index is not the only one. We can do GSA with the Borgnonovo index as well, this is supposed to take into account correlation between parameters - and in LCA many parameters are correlatd, e.g. use of coal and production of electricity. You can read more about:
# - The index itself in [Borgonovo (2007)](https://doi.org/10.1016/j.ress.2006.04.015): _A new uncertainty importance measure_ 
# - [How it is implemented in Salib](https://salib.readthedocs.io/en/latest/api.html#delta-moment-independent-measure) as _Delta Moment-Independent Measure_
# - and you can see an applicaiton in GSA for LCA models in [Blanco et al. (2020)](https://doi.org/10.1016/j.jclepro.2020.120968): _Assessing the sustainability of emerging technologies: A probabilistic LCA method applied to advanced photovoltaics_ 

# In[24]:


from SALib.sample import latin
from SALib.analyze import delta


# In[25]:


# Step 1. define parameters and their ranges in form of a problem
problem = { 'num_vars': 5, 
            'names': ['par0', 'par1', 'par2', 'par3', 'par4'], 
            'bounds': [[0, 1], [0, 1], # I am going to use percentiles for the first two  
                       [0.2*0.9, 0.2*1.1], [0.2*0.9, 0.2*1.1], # uniform disrribution for the other three
                       [0.2*0.9, 0.2*1.1]] } 


# In[26]:


# Step 2. Generate the samples
param_values = latin.sample(problem, 1000) # reduce this number for a fast test simulation!
print(param_values.shape)
param_values[0:5]


# As before, convert the first two in normal and lognormal respectively

# In[27]:


for i in param_values:
    i[0] = sp.stats.norm.ppf(i[0], 0.2, 0.01) #normal
    i[1] = sp.stats.lognorm.ppf(i[1], s = 0.1, scale = 0.2) #lognormal, see here:https://stackoverflow.com/questions/8870982/how-do-i-get-a-lognormal-distribution-in-python-with-mu-and-sigma
param_values[0:5]


# In[29]:


# Still step 3. Run these samples in our model and store the results in a list
GSA_el_value_results = []
for v in param_values:
    ActivityParameter.update(amount = v[0]).where(ActivityParameter.name == 'par0').execute()
    ActivityParameter.update(amount = v[1]).where(ActivityParameter.name == 'par1').execute()
    ActivityParameter.update(amount = v[2]).where(ActivityParameter.name == 'par2').execute()
    ActivityParameter.update(amount = v[3]).where(ActivityParameter.name == 'par3').execute()
    ActivityParameter.update(amount = v[4]).where(ActivityParameter.name == 'par4').execute()
    
    ActivityParameter.recalculate_exchanges("gsagroup")
    
    lca = bw.LCA({gsa_db.get('el_prod_for_sa') : 1}, ('IPCC 2013', 'climate change', 'global warming potential (GWP100)'))
    lca.lci()
    lca.lcia()
    GSA_el_value_results.append(lca.score)


# In[30]:


# Step 4. Feed the problem and the results to the Sobol function to obtain the Sobol indices 
D = delta.analyze(problem, param_values, np.array(GSA_el_value_results), print_to_console=True) # must use np.array
# Returns a dictionary with keys 'delta', 'delta_conf', 'S1', and 'S1_conf'
# (first and total-order indices with bootstrap confidence intervals)


# D (Delta) represents the normalized expected shift in the distribution of model output provoked by the parameter under analysis. Delta lies between 0 and 1 and it is zero when the model output is independent of the parameter.
# 
# In our case, Delta returns a similar result than the Sobol indices. Again the most sensitive parameter is _par4_ afollowed by _par3_ and _par2_.

# ### Questions for own reflection and plenum discussion
# 
# Could we have found the same results by looking just at the contribution analysis results?
# When do you think it is usueful to perform this simulation and for which parameters in your LCA model?

# ## Group exercise (we will do this in class): sensitivity analysis on the case studies.
# 
# Reflect about possible source of variance for your case study. Which activities are you unsure about? Are you in doubt about the type of activity used, or about the value used? Which activities do you expect to affect the results? Formulate some hypotheses based on your expectations and your understanding of your product system case. Then select the relevant parameters that could help you test these hypotheses and identify how sensitive are the results of your case study to these. Finally quantify this influence and rank the parameters based on their influence on the results.  
