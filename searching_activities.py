#%%
import bw2data as bd

bd.projects.set_current('cLCA-aalborg')
ei = bd.Database('con391')

search = ei.search("market for ammonium sulfate", filter={'location': 'RER'})

nh4so4_market = search[0]  # id = 17472

nh4so4_market = bd.get_node(id=17472)
nh4so4_market.as_dict()
# %%

print("The NH4SO4 market is consumed by:")
for consumer in nh4so4_market.consumers():
    print(consumer.output)

print("The NH4SO4 market is produced by:")
for producer in nh4so4_market.producers():
    print(producer.input)


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