#%% Import the necessary packages

import pandas as pd
import numpy as np
import bw2data as bd
import bw2calc as bc

# %% Define custom fuction to covert the dataframe from the csv into a set of dictionaries ready for the bw2io to make a database
#%% from Massimo 'lci_to_bw2.py'

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
    
    return bw2_db

def write_database(model):
    # apply the function to the dataframe to get a dictionary ready for bw2io
    db_name = 'fg_'+model
    db_df = pd.read_csv('data/{}.csv'.format(db_name), sep = ';')

    db = lci_to_bw2(db_df)

    # delete the database if it already exists
    try: 
        del bd.databases[db_name]
    except:
        pass

# write the database to the project
    fg = bd.Database(db_name)
    fg.write(db)
    
    #print("*******\n", fg.name, "\n", fg.metadata)

# check that it worked
    bd.databases
    fg.metadata
    fg_dict = fg.load()
    print(*fg_dict, sep = "\n")

# #%%  Inspect the database
# for act in fg:
#     dict = act.as_dict()
#     print("\n")
#     print("*****************************")
#     print("{} : {} : {}".format(dict['name'], dict["unit"], dict["code"]))
#     print("----------------------------")
#     print("TECHNOSPHERE EXCHANGES")
#     print(*list(act.technosphere()))
#     print("----------------------------")
#     print("BIOSPHERE EXCHANGES")
#     print(*list(act.biosphere()))
#     print("*****************************")
