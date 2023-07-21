#!/usr/bin/env python
# coding: utf-8

# # 2. How to navigate activities and exchanges in Brightway2

# When you do an LCA you need to access the various activities and look at them to understand what are their inputs and outputs and how they are linked to other activities. This script includes code to do this in different ways. Try it out and try it on your own product system as well. 

# In[1]:


import brightway2 as bw


# In[2]:


bw.projects.set_current('advlca23')  # created in the previous notebook


# In[3]:


bw.databases  # should have the two databases: "testdb" and "testbiosphere"


# In[4]:


t_db = bw.Database('testdb') # We create an instance of this database class


# First we look into the information associated with a **specific activity**.
# This is how we select the activity (a DICT):

# In[5]:


el = t_db.get('Electricity production')  # reads: "get the activity electricity production from t_db 
                                         # and call it el"
print(el)


# In[6]:


for k in el:  # k for "key". These the possible keys of an activity dictionary
    print(k)


# In[7]:


el.as_dict()  # or just this (type '.' and then press 'tab')


# In[8]:


print(el['name'])  # print the value of one key

print(el['name'], "***", el['code'], "***", el['unit'], "***", el['database'])  # print more than one...

print(el.get('unit'))  # another way...


# Now instead we look at the **exchanges** of a specific activity

# In[9]:


#el['exchanges']  # this doesn't work.
#el.exchanges()  # neither this
list(el.exchanges())  # yeps, this one


# In[10]:


for exc in el.exchanges():  # or this, visualize all exchanges of an activity and specific attributes
    print(exc)
    print(exc['type'])
    print(exc['input'][0])
    print(exc.input)
    print("-------")


# Now we look at the information associated with a specific **exchange** of a specific activity

# In[11]:


el_exc = list(el.exchanges())[0]  # "the first exchange of the el activity" (this is also a DICT)
print(el_exc)


# In[12]:


print(type(el))  # compare the three
print(type(el.exchanges()))
print(type(el_exc))


# In[13]:


for i in el_exc:  # the possible keys of an exchange (DICT iteration)
    print(i, ':', el_exc[i])


# In[14]:


el_exc.as_dict()  # or just this, as above


# In[15]:


el_exc.items() # another nice one


# In[16]:


el_exc.unit == el_exc['unit']  # equivalent ways, different from activities


# In[17]:


print(el_exc['amount'], el_exc['unit'], el_exc['input'], 
      '\nto\n',
      el_exc['output'], 
      '\nwithin\n', 
      el_exc['type'])


# In[18]:


print(el_exc.input)  # One can intended the word 'input' as "from'
print(el_exc.output)  # ...and 'output' as 'to'


# What if I want to get a specific exchange of a specific activity **without using numeric indexing**, but by using its name? Let's see if we can find the amount of Carbon Dioxide emitted from electricity production
# 

# In[19]:


for exc in list(el.exchanges()):
    if exc['input'] == ('testbiosphere', 'Carbon dioxide'):
        print(exc)
    else:
        print(exc['input'][1],'...Not this one')


# Good. Now we store the value **in a variable** for future use

# In[20]:


for exc in list(el.exchanges()):
    if exc['input'] == ('testbiosphere', 'Carbon dioxide'):
        elCO2_amount = exc['amount'] # creates the variable elCO2amount

print(elCO2_amount)


# In[21]:


elCO2_amount * 1234.56  # it's a number and you can make operations with that

