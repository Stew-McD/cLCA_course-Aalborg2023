#%% 
import graphviz as gv
import bw2data as bd

#%% initialise the graph object

g = gv.Digraph(
                filename="SuccinicAcidmarket", 
                #engine='twopi', 
                format='svg',
                graph_attr={'rankdir':'LR',
                            'pad': '0.1',
                }) 

#%% load the project and define the databases

bd.projects.set_current('cLCA-aalborg')
fg = bd.Database('fg_csv')
bio = bd.Database('biosphere3')

#%%
# pull the activities and flows input the database
edges = []
nodes = []

# extract the flows (edges)
for act in fg:
    for ex in act.exchanges():
        ex = ex.as_dict()
        input = bd.get_node(code=ex['input'][1]).as_dict()
        output = bd.get_node(code=ex['output'][1]).as_dict()
        edge = {'input': input["name"], 
                'output': output["name"], 
                'amount': ex['amount'], 
                'unit': ex['unit'],
                'type' : ex['type'],
                'db_input' : input['database'],
                'db_output' : output['database'],
                'PFD_weight': 0}

        if input != output: edges.append(edge)
#%%
# extract the activities (nodes)
nodes = []
for edge in edges:
    node = {'name': edge['input'], 'db': edge['db_input'], 'type' : edge['type']}
    if node not in nodes:
        nodes.append(node)
    if node not in nodes:
        nodes.append(node)

#%%

for act in nodes:
    g.node(act['name'], label=act['name'], shape='box')
    
    if act['db'] == 'con391':
        g.node(act['name'], color='blue')
    elif act['db'] == 'fg_csv':
        g.node(act['name'], color='red')
    elif act['db'] == 'biosphere3':
        g.node(act['name'], color='green', label=act['name'], shape='ellipse', style='filled', fontcolor='white',
        )
    
    if act['name'] == 'Succinic acid production':
        g.node(act['name'], color='pink', shape='ellipse', style='filled')

    try: 
        g.node(act['name'], pos=act['PFD_pos'])
    except KeyError:
        pass

    try:
        g.node(act['amount'], size=act['PFD_size'])
    except KeyError:
        pass


for edge in edges:
    if edge['unit'] == 'm3': edge['unit'] = 'm³' #  
    #if edge['unit'] == 'm3': edge['unit'] = "m\u00B2" # wtf? 

    if 'PFD_weight' not in edge:
        edge['PFD_weight'] = 0
    
    g.edge(tail_name=edge['input'], 
            head_name=edge['output'], 
            label="{:.2E} {}".format(edge['amount'] , edge['unit']),
            penwidth=str(0.1+(edge['amount'])**0.1),
            weight=str(edge['PFD_weight']),
            #edge_attr={"weight" : str(edge['PFD_weight'])}
            )


g.render()

g