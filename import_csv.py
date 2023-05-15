#%% import a database from a csv file using the custom script from Massimo

import pandas as pd
import numpy as np
import bw2data as bd

#%% Define custom fuction to import transform a df into a database: from Massimo 'lci_to_bw2.py'


def lci_to_bw2(mydb):
    '''A function to convert a pd.Dataframe to a dict
    to be used as database in bw2'''
    
    act_keys_raw = list(mydb.columns[0:5])
    act_keys_bw2 = [i.replace('Activity ','') for i in act_keys_raw]
    
    exc_keys_raw = list(mydb.columns[5:])
    exc_keys_bw2 = [i.replace('Exchange ','') for i in exc_keys_raw]
    
    def exc_to_dict(df_data, some_list):
        exc_data = (pd.DataFrame(list(df_data.values), index = list(exc_keys_bw2))).T
        exc_data = exc_data.dropna(axis=1, how='any') # remove columns withouth the data
        e_values = (exc_data.values).tolist()[0]
        e_values = [(e_values[0],e_values[1])] + e_values[2:]
        some_list.append(dict(zip(list(exc_data.columns)[1:], e_values)))
        
    def act_to_dict(act_data):
        a_keys = act_keys_bw2[2:] + ['exchanges']
        return dict(zip(a_keys, act_data))
    
    def bio_to_dict(bio_data):
        b_keys = act_keys_bw2[2:]
        return dict(zip(b_keys, bio_data))
        
    
    db_keys = []
    db_values =[]
    
    for act in mydb['Activity name'].unique():
    
        sel = mydb[mydb['Activity name'] == act]
        db_key = (list(sel['Activity database'])[0], list(sel['Activity code'])[0])
        db_keys.append(db_key)
        
        if list(sel['Activity type'].unique())[0] == 'biosphere':
                    
            my_bio_data = list(sel.iloc[0,2:5].values)
            db_value = bio_to_dict(my_bio_data)
            db_values.append(db_value)
        
        else:
            my_exc = []
            for i in range(sel.shape[0]):
                exc_to_dict(sel.iloc[i,5:],my_exc)
            
            my_act_data = list(sel.iloc[0,2:5].values) + [my_exc]
            db_value = act_to_dict(my_act_data)
            db_values.append(db_value)
        
     
    bw2_db = dict(zip(db_keys, db_values))
    
    return bw2_db # We have a dict to be used as database. Perfect.
# %%



mydb = pd.read_csv('data/foreground.csv', header = 0, sep = ";")
mydb.head()

mydb.replace("exldb", "fg_csv", inplace=True)
mydb.replace("biosphere3", "biosphere", inplace=True)
mydb.replace("ecoinvent 3.9 conseq", "con391", inplace=True)

mydb['Exchange amount'] = mydb['Exchange amount'].str.replace(',', '.').astype(float)

mydb = mydb.drop('Notes', axis = 1)
mydb['Exchange uncertainty type'] = mydb['Exchange uncertainty type'].fillna(0)
mydb.head()
db = lci_to_bw2(mydb)
bd.projects.set_current('cLCA-aalborg')
bd.databases

fg = bd.Database('fg_csv')
fg.write(db)
bd.databases
fg.metadata
fg_df = fg.load()

#%%
for act in db:
    print(act[1])

# In[13]:
nacl = fg.get('NaCl production')
nacl.as_dict()

[print(act, act.as_dict()['amount']) for act in fg] 
 # check more stuff 
print('---------')


[[print(act, exc) for exc in list(act.technosphere())]for act in fg]  # check more stuff 
print('---------')
[[print(exc.uncertainty) for exc in list(act.biosphere())]for act in fg]  # check more stuff

#%%

myact = bw.Database("exldb").get('Fuel production')
list(myact.exchanges())

#%%


mymethod = ('IPCC 2013', 'climate change', 'global warming potential (GWP100)')
el = fg.get("Electricity production")
functional_unit = {el: 1000}
lca = bw.LCA(functional_unit, mymethod)
lca.lci()
lca.lcia()
print(lca.score)