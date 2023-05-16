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