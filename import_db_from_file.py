#%% Import the necessary packages

import pandas as pd
import numpy as np
import bw2data as bd

# %% Define custom fuction to covert the dataframe from the csv/excel into a set of dictionaries ready for the bw2io to make a database
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
        # This code extracts the values of the exc_data dataframe and stores them in the e_values variable.
        e_values = (exc_data.values).tolist()[0]

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
    
    for act in db_df['Activity code'].unique():
    
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
    print("\n==================\n Writing database for: {}\n==================".format(model))
    # apply the function to the dataframe to get a dictionary ready for bw2io
    db_name = 'fg_'+model
# you can choose if you want to import from a csv or an excel file
    # db_df = pd.read_csv('data/{}.csv'.format(db_name), sep = ';')
    db_df = pd.read_excel('data/{}.xlsx'.format(db_name))
    db_df
    db = lci_to_bw2(db_df)

    # delete the database if it already exists
    try: 
        del bd.databases[db_name]
        print("\nDeleted old database {}".format(db_name))
    except:
        print("\nDatabase {} does not exist".format(db_name))
        pass

# write the database to the project
    print("\n****** Writing new database: {}".format(db_name))
    fg = bd.Database(db_name)
    fg.write(db)
    
# check that it worked
    # bd.databases
    print(fg.metadata)
    fg_dict = fg.load()

    return fg_dict
    #print(*fg_dict, sep = "\n")

# #%%  Inspect the database

def inspect_db(db):
    for act in db:
        dict = act.as_dict()
        print("   ACTIVITY:  ")
        print("*****************************")
        print("{} : {} : {}".format(dict['name'], dict["unit"], dict["code"]))
        print("----------------------------")
        print("TECHNOSPHERE EXCHANGES:", len(list(act.technosphere())))
        [print(' * ',x) for x in list(act.technosphere())]
        print("----------------------------")
        print("BIOSPHERE EXCHANGES: ", len(list(act.biosphere())))
        [print(' * ',x) for x in list(act.biosphere())]
        print("*****************************")
