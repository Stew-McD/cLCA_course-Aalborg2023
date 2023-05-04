

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