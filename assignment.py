

#%%
import bw2data as bd

bd.__version__

# %%

bd.projects.set_current("cLCA-aalborg")

db = bd.Database("con391")

# %%

act_list_ei = ["bacterial fermentation", "purification"] 

bac_ferm = db.search(act_list_ei[0])
bac_pur = db.search(act_list_ei[1])

print(bac_ferm)
print(bac_pur)

bio = bd.Database("biosphere3")

ch4 = bio.search("methane")[0]
ch4.as_dict()

ch = bio.search("Chromium VI")
ch

so2  = bio.search("sulfur dioxide")[4]
so2.as_dict()

# nothing found
# %% CREATE A NEW DATABASE AND ADD THE FOREGROUND

# make a new database

db_fore = bd.Database("foreground")

#%%
# add activities to a custom database 

bac_ferm = db_fore.new_node = ({ 
"name" : "bacterial fermentation", 
"code" : "bac_ferm",
"unit": "kg"
})
bac_ferm.save()

# write a function to multiply
