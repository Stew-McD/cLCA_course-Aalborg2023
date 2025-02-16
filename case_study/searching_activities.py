"""
# searching_activities.py

This script demonstrates how to search for specific activities in the `con391` and `biosphere3` databases using the Brightway2 package.

The script first sets the current project to `cLCA-aalborg` and creates two database objects, `ei` and `bio`, which represent the `con391` and `biosphere3` databases, respectively.

It then searches for specific activities in the `ei` and `bio` databases and prints out information about those activities.

Author: Stew-McD
Date: 27/05/2023
"""


"""
This Python code is using the Brightway2 package to search for specific activities in the con391 and biosphere3 databases. Here's a breakdown of what each section of the code is doing:

The first few lines of code import the bw2data package and set the current project to cLCA-aalborg. It then creates two database objects, ei and bio, which represent the con391 and biosphere3 databases, respectively.

The next few lines of code search for a specific activity in the ei database with the name "market for ammonium sulfate" and the location "RER". It then retrieves the first search result and assigns it to the variable nh4so4_market. Finally, it prints out the dictionary representation of the nh4so4_market node.

The next section of code creates a list of activity names and splits it into individual strings. It then searches for each activity in the bio database and prints out the name, location, and code of each activity that is found. If an activity is not found, it prints out the message "not found".

The next section of code searches for a specific activity in the ei database with the name "tilapia feed production, commercial" and the location "RoW". It then retrieves the first search result and prints out a list of all the inputs to the activity.

The next section of code searches for a specific activity in the ei database with the name "market for soybean meal" and the location "RoW". It then retrieves the first search result and prints out the dictionary representation of the activity.

The next section of code searches for a specific activity in the ei database with the name "market for ammonium". It then prints out the name, location, and code of each search result.

The final section of code searches for a specific activity in the bio database with the name "methane, non-fossil" and the category "air". It then retrieves the second search result and prints out the dictionary representation of the activity. 

"""

#%%
import bw2data as bd

bd.projects.set_current('cLCA-aalborg')
ei = bd.Database('con391')
bio = bd.Database('biosphere3')

search = ei.search("market for ammonium sulfate", filter={'location': 'RER'})

nh4so4_market = search[0]  # id = 17472

nh4so4_market = bd.get_node(id=17472)
nh4so4_market.as_dict()
# %%
acts = " Volatile organic compund,Carbon monoxide,Particulates <10 um,Ammonia,Lead,Sulfuric acid,Waste water,Cell mass,Sorghum grain waste,Sorghum grains,Dextrose,Process water,Ultrapure water,Electricity,Natural gas for steam,Ammonium Liquid"

acts = acts.split(",")

a = ei.search("sorghum")
a
a[3].as_dict()["code"]

for act in acts:
    
    print(act)
    try:
        a =bio.search(act)[0].as_dict()
        #print(a)
        print(a['name'], a['location'], a["code"])
    except:
        print("\t not found")
# %%
#
fish = ei.search("tilapia feed production, commercial",
                 filter={'location': 'RoW'})[0]

list(fish.technosphere())


# %%
soy = ei.search("market for soybean meal", filter={'location': 'RoW'})[0]

soy.as_dict()

#%% Search for a specific activity and find the code in the ei database
ei = bd.Database("con391")
act = ei.search("market for ammonium")
# look at the results
for a in act:
    print(a['name'], a['location'], a["code"])
# 
act[0].as_dict()
#%% Search for a specific activity and find the code in the biosphere database
bio = bd.Database("biosphere3")
act = bio.search("methane, non-fossil", filter={'categories': 'air'})
act
act[1].as_dict()