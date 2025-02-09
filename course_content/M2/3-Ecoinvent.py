#!/usr/bin/env python
# coding: utf-8

# # 3. Import biosphere3 and ecoinvent

# Now that you know how to work with the foreground system, it's time to learn how to work with the background system. In particular it is useful to import and play around with two databases: _biosphere3_ that contains all the exchanges and impact assessment methods, and _ecoinvent_. You need to get the ecoinvent files first, see steps below:
# 
# 1. Open the ecoinvent website and [login](https://www.ecoinvent.org/login-databases.html) with your username and password.
# 2. You should read somewhere: _To download LCI and LCIA cumulative matrices click here_. Click there.
# 3. Select _ecoinvent 3.6._
# 4. Download the file `ecoinvent 3.9_consequential_ecoSpold02.7z` in a folder of yours. Make sure you remember the full path to this directory. E.g. I have downloaded the file in:
# _/Users/massimo/Documents/Databases/ecoinvent v3.9_
# 5. The file you have downloaded is a compressed archive of many files (like with winzip or winrar). Extract the files from the .7z archive, e.g. by double clicking it. If it does not work, install a software that can do that. E.g. for mac users you can either download [theunarchiver](https://theunarchiver.com/) or, if you are using brew, just open terminal and do `brew install p7zip` and then from terminal find the folder and do `7z x 'ecoinvent 3.9_consequential_ecoSpold02.7z'` (here the [p7zip instructions](https://wiki.archlinux.org/index.php/p7zip) in case).
# 6. Now you an run the cells below. Make sure you change the path line and replace it with the one where you have extracted the files. For example, I have extracted the files in a folder called "datasets". The path to this folder is: _/Users/massimo/Documents/Databases/ecoinvent v3.6/datasets_ You will see this same line in the script and you need to change it with your directory. 

# In[1]:


import brightway2 as bw


# In[2]:


bw.projects # check what project you have 
#bw.projects.delete_project('advlca23', delete_dir=True) # if you want a fresh start


# In[3]:


bw.projects.set_current('advlca23') # Still working in the same project
bw.databases
#bw.databases.clear() # For a fresh start (Risky command! clears all your existing databases)


# Before importing ecoinvent, we need to make a default setup of Brightway2. This means importing all the environmental exchanges and all the LCIA methods. Then when we import ecoinvent the ecoinvent activities will be linked to this database of environmentla exchanges, just like in the previous example wiht the product system of H&S 2002.

# In[4]:


# Import the biosphere3 database
bw.bw2setup() # This will take some time


# We are going to use version 3.9 of ecoinvent, consequential model, for this course.

# In[5]:


# Import ecoinvent

# You need to change the line below with the "datasets" directory where you have extracted ecoinvent files
ei39dir = "/Users/massimo/Documents/Databases/ecoinvent v3.9.1/ecoinvent 3.9.1_consequential_ecoSpold02/datasets"

if 'ecoinvent 3.9 conseq' in bw.databases:
    print("Database has already been imported")
else:
    ei39 = bw.SingleOutputEcospold2Importer(ei39dir, 'ecoinvent 3.9 conseq') # You can give it another name of course
    ei39.apply_strategies()
    ei39.statistics()

#ei39.drop_unlinked(True)
ei39.write_database() # This will take some time.


# In[6]:


bw.databases # you should now see both "biosphere3" and "ecoinvent 3.9 conseq"


# # Navigate biosphere3 and ecoinvent

# A key difference compared to previous exercises is that in ecoinvent each activity and exchange is defined by a **code** which are unique identifiers. So it is important to learn how to find both activity code and name and how to match them _(Actually we used the codes also in the previous lectures but they were identical to the activity names for simplicity)_.

# In[7]:


# Search stuff in biosphere
bw.Database("biosphere3").search("carbon dioxide") # there is more than one activity with this name. Only code is univocal.


# In[8]:


CO2 = bw.Database("biosphere3").get("349b29d1-3e58-4c66-98b9-9d1a076efd2e") # This code works across bw2 installations, 
                                                                    ### i.e. is univocal for biosphere3 everywhere
print(CO2['name']) # there is more than one activity with this name. Only code is univocal.
print(CO2['code'])


# In[10]:


# Search stuff in ecoinvent

# Search by keyword
mydb = bw.Database('ecoinvent 3.9 conseq')
#mydb.search("*") # to search everything
mydb.search("transport freight euro5")

#bw.Database('ecoinvent 3.9 conseq').search("transport") # gives the same result obviously


# In[11]:


activity_name = 'electricity'

# Same but different:
for activity in bw.Database("ecoinvent 3.9 conseq").search(activity_name, limit = 5):  
    print(activity)
    print(activity['code'])


# In[13]:


# Try this        
for activity in bw.Database("biosphere3").search("transport"):  
    print(activity)
    print(activity['code']) # Can you explain this result?


# In[14]:


# you can be much more specific in your search:
for activity in bw.Database("ecoinvent 3.9 conseq").search(activity_name, filter={"location" : 'DK'}, limit = 5):
    print(activity)
    print(activity['code'])


# Now you know how to find activities. What about **selecting** activities?

# In[17]:


# If you know the code (e.g. found with method above) it's simple.        
mycode = 'ce40dd006e462e720eb669efbc31dd59'
myact = bw.Database("ecoinvent 3.9 conseq").get(mycode)
#myact = Database("biosphere3").get(mycode)  # Not working of course...

print(myact['name'])


# In[18]:


myact._data # a lot of detail


# In[19]:


for i in list(myact.exchanges()):  # Epxlore the activity as usual
    print(i['type'])
    print(i)
    print(i['input'])
    print('-------')


# In[20]:


# If you know the name and want to select it:
activity_name = 'market for electricity, low voltage'
    
for activity in bw.Database("ecoinvent 3.9 conseq"):  # can you find an easier way? I couldn't
    if activity['name'] == activity_name:
        myact = bw.Database("ecoinvent 3.9 conseq").get(activity['code'])

myact  # Careful! Might not return the danish market. Not what I wanted! 


# In[21]:


for activity in bw.Database("ecoinvent 3.9 conseq"):  
    if activity['name'] == activity_name and activity['location'] == "DK":  # need to be specific...
        myact = bw.Database("ecoinvent 3.9 conseq").get(activity['code'])
myact  # alright


# # Calculate with biosphere3 and ecoinvent 
# 
# Ok now we can run an LCA with a dataset from ecoinvent.

# In[30]:


list(bw.methods)


# In[31]:


# First select a method from the list (use 'list(methods)' to see all of them)
mymethod = ('IPCC 2013', 'climate change', 'global warming potential (GWP100)')
mymethod


# In[32]:


myact = bw.Database("ecoinvent 3.9 conseq").get('ce40dd006e462e720eb669efbc31dd59')
myact


# In[33]:


functional_unit = {myact : 1}
lca = bw.LCA(functional_unit, mymethod) #run LCA calculations again with method
lca.lci()
lca.lcia()
print(lca.score) # What is the unit? Find out! (alright it's bw.methods[mymethod])


# In[34]:


bw.methods[mymethod]


# # Exercise (at home)
# Link the emissions of your previously defined foreground system to the biosphere3 database, and link some of the ecoinvent database activities to your foreground system. Run the calculations and get a carbon footprint with the ILCD climate change method.
