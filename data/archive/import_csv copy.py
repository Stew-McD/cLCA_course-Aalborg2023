#%% Import the necessary packages

import pandas as pd
import numpy as np
import bw2data as bd
import bw2calc as bc

#%% Define custom fuction to covert the dataframe from the csv into a set of dictionaries ready for the bw2io to make a database
# from Massimo 'lci_to_bw2.py'

def lci_to_bw2(db_df):
    '''A function to convert a pd.Dataframe to a dict
    to be used as database in bw2'''
    
    act_keys_raw = list(db_df.columns[0:5])
    act_keys_bw2 = [i.replace('Activity ','') for i in act_keys_raw]
    
    exc_keys_raw = list(db_df.columns[5:])
    exc_keys_bw2 = [i.replace('Exchange ','') for i in exc_keys_raw]
    
    def exc_to_dict(df_data, some_list):
        exc_data = (pd.DataFrame(list(df_data.values), index = list(exc_keys_bw2))).T
        exc_data = exc_data.dropna(axis=1, how='any')
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
    
    for act in db_df['Activity name'].unique():
    
        sel = db_df[db_df['Activity code'] == act]
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
# %% Import the csv file and convert it to a database
db_df = pd.read_csv('data/Inventory_data_brightway2.csv', header = 0, sep = ";")
db_df.head()

cols = ['Activity database', 'Activity code', 'Activity name', 'Activity unit',
       'Activity type', 'Exchange database', 'Exchange input',
        'Exchange unit', 'Exchange type',
       ]

names = ['Activity code', 'Activity name', 'Exchange input']
#%%
for col in names:
    print("\n*****\n***", col , len(db_df[col].unique()))
    print(*sorted(db_df[col].unique()))

#%%

db_df.replace("Technosphere", "technosphere", inplace=True)
db_df.replace("Biosphere", "biosphere", inplace=True)

db_df.replace("exldb", "fg_csv", inplace=True)
db_df.replace("MgCO2", "MgCO3", inplace=True)
db_df.replace("HCL", "HCl", inplace=True)
# db_df.replace("biosphere3", "biosphere", inplace=True)
db_df.replace("ecoinvent 3.9 conseq", "con391", inplace=True)

# db_df['Exchange amount'] = db_df['Exchange amount'].str.replace(',', '.').astype(float)

#db_df = db_df.drop('Notes', axis = 1)
db_df["comment"] = ""
db_df['Exchange uncertainty type'] = db_df['Exchange uncertainty type'].fillna(0)
db_df.replace("nan", 0.0, inplace=True)
db_df.replace(np.NaN, 0.0, inplace=True)
db_df.replace(0, 0.0, inplace=True)
db_df.head()
#%%
ei = bd.Database('con391')
bio = bd.Database('biosphere3')
for i, act in db_df.iterrows():
    #print("\n*** ", act.loc["Activity name"], act.loc["Exchange input"], act.loc["Exchange type"])
    try:
        x = ei.get(code=act.loc["Exchange input"]).as_dict()
        #print(x['database'], " \t", x['name'], "\t", x['type'])
    except:
        try:
            x = bio.get(code=act.loc["Exchange input"]).as_dict()
            #print(x['database'], " \t", x['name'], "\t", x['type'])
        except:
            print("\n*** ", act.loc["Activity name"], act.loc["Exchange input"], act.loc["Exchange type"])
            print("Not found")
            pass

db = lci_to_bw2(db_df)


#%% Create a new database in brightway
bd.projects.set_current('cLCA-aalborg')
bd.databases

try: 
    del bd.databases['fg_csv']
except:
    pass

fg = bd.Database('fg_csv')
fg.write(db)
bd.databases
fg.metadata
fg_df = fg.load()

act = bd.get_node(code='d068f3e2-b033-417b-a359-ca4f25da9731')
act
#%%
for act in fg:
    dict = act.as_dict()
    print("\n\n")
    print("*****************************")
    print("{} : {} : {}".format(dict['name'], dict["unit"], dict["code"]))
    print("----------------------------")
    print("TECHNOSPHERE EXCHANGES")
    print(*list(act.technosphere()))
    print("----------------------------")
    print("BIOSPHERE EXCHANGES")
    print(*list(act.biosphere()))


#%%
[print(act, act.as_dict()) for act in fg] 
 # check more stuff 
print('---------')


[[print(act, exc) for exc in list(act.technosphere())]for act in fg]  # check more stuff 
print('---------')
[[print(exc.uncertainty) for exc in list(act.biosphere())]for act in fg]  # check more stuff

#%%

myact = bd.Database("exldb").get('Succinic acid production')
list(myact.exchanges())

#%%

feed

mymethod = ('IPCC 2013', 'climate change', 'global warming potential (GWP100)')
sa = fg.get("Succinic acid production")
functional_unit = {sa: 1}
lca = bc.LCA(functional_unit, mymethod)
lca.lci()
lca.lcia()
print(lca.score)
# %%

gwp = 