#%%
#%% initialise the graph object
def extract_nodes_edges(model):

    import bw2data as bd

    #% load the project and define the databases
    db_name = 'fg_'+model
    bd.databases
    bd.projects.set_current('cLCA-aalborg')
    fg = bd.Database(db_name)
    bio = bd.Database('biosphere3')

    #%
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
            
            if edge['unit'] == 'm3': edge['unit'] = 'm³'

            if input != output: edges.append(edge)
    #%
    # extract the activities (nodes)
    nodes = []
    for edge in edges:
        node = {'name': edge['input'], 'db': edge['db_input'], 'type' : edge['type']}
        if node not in nodes:
            nodes.append(node)
        if node not in nodes:
            nodes.append(node)
    
    return nodes, edges, model
nodes, edges, model = extract_nodes_edges('corn')
#%%


def make_process_diagram(model):
    # initialise the graph object
    import graphviz as gv
    g = None
    g = gv.Digraph(
                filename="inventory/SuccinicAcid_Inventory_{}".format(model), 
                engine='dot', 
                format='png',
                graph_attr={'rankdir':'RL',
                            'pad': '0.1',
                            # 'splines':'curved',
                            # 'overlap':'prism',
                            # 'nodesep':'0.1',
                            # 'ranksep':'0.1',
                            # 'fontname':'Arial',
                            # 'fontsize':'20',
                            # 'fontcolor':'black',
                            # 'bgcolor':'transparent',
                            # 'margin':'0',
                            # 'compound':'true',
                            # 'dpi':'300',
                            # 'ratio':'0.5',
                            # 'size' : '2,5',
                            # "size" : "8,5",
                })
    
    # make the first cluster for the background flows
    with g.subgraph(name='cluster_bg') as bg:
        bg.attr(label='Background flows', labelloc='t', fontsize='20', fontcolor='black', style='solid', color='black', shape='box', rank='min',rankdir='TB',penwidth='2', xfontcolor='black')

        for act in nodes:
            if act['db'] == 'con391':
                bg.node(act['name'], fillcolor='#ff000080', label=act['name'], shape='box', style='filled', fontcolor='black'
                )
    
    # make the second cluster for the foreground flows
    with g.subgraph(name='cluster_fg') as fg:

        fg.attr(label='Foreground flows', labelloc='t', fontsize='20',          style='solid', fontcolor='black', color='black', alpha='0.1',shape='box',   rank='max',rankdir='TB',penwidth='2',xfontcolor='black')

        for act in nodes:
            if 'fg' in act['db'] :
                fg.node(act['name'], color='blue', label=act['name'], shape='box', style='filled', fontcolor='white'
                )

    # make the third cluster for the biosphere flows
    with g.subgraph(name='cluster_bio') as bio:
        
        bio.attr(label='Biosphere flows', labelloc='t', fontsize='20', style='solid', penwidth='2', xfontcolor='black', color='black', alpha='0.1', shape='box', rank='sink',rankdir='TB')

        for act in nodes:
            if act['db'] == 'biosphere3':
                bio.node(act['name'], color='green', label=act['name'], shape='ellipse', style='filled', fontcolor='black'
                )

    # make links between the nodes

    for edge in edges:
        if edge['db_input'] == 'biosphere3': 
                direction='back'
                g.edge(tail_name=edge['input'], 
                        head_name=edge['output'], 
                        xlabel="{:.1e} {}".format(edge['amount'] , edge['unit']),
                        fontsize='8',
                        penwidth=str(0.1+(edge['amount'])**0.1),
                        weight=str(edge['PFD_weight']),
                        dir=direction,
                        #edge_attr={"weight" : str(edge['PFD_weight'])}
                        )      
        elif edge['db_input'] == 'con391':
                direction='forward'
                g.edge(tail_name=edge['input'], 
                        head_name=edge['output'],
                        fontsize='8',
                        xlabel="{:.1e} {}".format(edge['amount'] , edge['unit']),
                        penwidth=str(0.1+(edge['amount'])**0.1),
                        weight=str(edge['PFD_weight']),
                        dir=direction,
                        #edge_attr={"weight" : str(edge['PFD_weight'])}
                        )
                
        elif edge['db_input'] == 'fg_'+model:
                direction='forward'
                g.edge(tail_name=edge['input'], 
                        head_name=edge['output'],
                        fontsize='8',
                        xlabel="{:.1e} {}".format(edge['amount'] , edge['unit']),
                        penwidth=str(0.1+(edge['amount'])**0.1),
                        weight=str(edge['PFD_weight']),
                        dir=direction,
                        #edge_attr={"weight" : str(edge['PFD_weight'])}
                        )

    g.render()
    return g

pfd = make_process_diagram(model)
pfd
        #%%

        for edge in edges:
             #  
            #if edge['unit'] == 'm3': edge['unit'] = "m\u00B2" # wtf? 

            if 'PFD_weight' not in edge:
                edge['PFD_weight'] = 0.1
            
                    # change arrow direction for biosphere flows
            

            elif act['db'] == 'con391':
                g.node(act['name'], label=act['name'], shape='box', color='blue', style='filled', fontcolor='white')
                

            elif 'fg' in act['db'] :
                g.node(act['name'], color='red')
                
                if 'Succinic acid production' in act['name']:
                    g.node(act['name'], color='pink', shape='ellipse', style='filled')

            try: 
                g.node(act['name'], pos=act['PFD_pos'])
            except KeyError:
                pass

            try:
                g.node(act['amount'], size=act['PFD_size'])
            except KeyError:
                pass
            else:
                direction='forward'

            g.edge(tail_name=edge['input'], 
                    head_name=edge['output'], 
                    label="{:.2f} {}".format(edge['amount'] , edge['unit']),
                    penwidth=str(0.1+(edge['amount'])**0.1),
                    weight=str(edge['PFD_weight']),
                    dir=direction,
                    #edge_attr={"weight" : str(edge['PFD_weight'])}
                    )
            
            g.render()
            g
# %

if __name__ == "__main__":
    models = ["corn", "bread"]
    for model in models: 
        make_process_diagram(model)