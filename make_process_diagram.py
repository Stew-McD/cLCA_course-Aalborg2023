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
            edge = {'input': input["name"].split(",")[0], 
                    'output': output["name"].split(",")[0], 
                    'amount': ex['amount'], 
                    'unit': ex['unit'],
                    'type' : ex['type'],
                    'db_input' : input['database'],
                    'db_output' : output['database'],
                    'PFD_weight': 0}
            
            if edge['unit'] == 'm3': edge['unit'] = 'm³'
            edges.append(edge)

    #%
    # extract the activities (nodes)
    nodes = []
    for edge in edges:
        node = {'name': edge['input'].split(",")[0], 'db': edge['db_input'], 'type' : edge['type']}
        if node not in nodes:
            nodes.append(node)

    return nodes, edges, model

#%%
def write_process_diagram(nodes, edges, model, scenario_name):
    # initialise the graph object
    import graphviz as gv
    import numpy as np
    g = None
    g = gv.Digraph(
                filename="inventory/SuccinicAcid_Inventory_{}_{}".format(model, scenario_name), 
                engine='dot', 
                format='svg',
                graph_attr={
                            'label':'System model for succinic acid production from {} - {}'.format(model, scenario_name),
                            'labelloc':'t',
                            'rankdir':'TB',
                            'pad': '.5',
                            # 'nodesep':'0.5',
                             'edgesep':'2',
                            'splines':'ortho',
                            # 'overlap':'false',
                            'fontname':'Comic Sans MS',
                            'fontsize':'30',
                            # 'fontcolor':'black',
                            #'bgcolor':'#00000',
                            'margin':'0',
                            # 'compound':'true',
                            # 'dpi':'300',
                            # 'ratio':'0.5',
                            # 'size' : '2,5',
                            # "size" : "8,5",
                })
    
    # make the first cluster for the background flows
    with g.subgraph(name='cluster_fg') as bg:
        
        # bg.attr(label='Technosphere flows', labelloc='t', fontsize='20', fontcolor='black', style='solid', color='black', shape='box', rank='min',rankdir='TB',penwidth='2', xfontcolor='black')


        for act in nodes:
            if act['db'] == 'con391':
                bg.node(act['name'], fontname='Comic Sans MS', fillcolor="darkolivegreen", label=act['name'], shape='box', style='filled', fontcolor='white', alpha='0.5'
                )
    
    # make the second cluster for the foreground flows
    with g.subgraph(name='cluster_fg') as fg:

        fg.attr(label='', margin='30', labelloc='t', fontsize='20', fontname='Comic Sans MS', style='solid', fontcolor='white', fillcolor='darkorchid2', alpha='0.6', shape='box',   rank='max',rankdir='TB',penwidth='2',xfontcolor='black')

        # fg.attr(penwidth='2', xfontcolor='black', color='white', alpha='0.1', shape='none', rank='sink',rankdir='TB')

        for act in nodes:
            if 'fg' in act['db'] :
                fg.node(act['name'], label=act['name'], shape='box', style='filled', fontname='Comic Sans MS', fontcolor='white', alpha='0.5', fillcolor='#0a86e5',
                )

                if 'Succinic acid production' in act['name']:
                    fg.node(act['name'], color='green', shape='ellipse', style='filled', fillcolor='#471a87', fontcolor='white', alpha='0.5')
                
                if 'Bread waste' in act['name']:
                    fg.node(act['name'], color='rgb(189, 177, 5)', shape='ellipse', style='filled', fillcolor='goldenrod', fontcolor='white', alpha='0.5')

                

    # make the third cluster for the biosphere flows
    with g.subgraph(name='cluster_bio') as bio:
        
        # bio.attr(label='Biosphere flows', labelloc='t', fontsize='20', style='solid', penwidth='2', xfontcolor='black', color='black', alpha='0.1', shape='box', rank='sink',rankdir='TB')

        for act in nodes:
            if act['db'] == 'biosphere3':
                bio.node(act['name'], fillcolor='green3', label=act['name'], shape='ellipse', style='filled', fontcolor='black'
                )

    # make links between the nodes

    for edge in edges:
        if edge['amount'] == 0: continue
        if edge['db_input'] == 'biosphere3': 
                direction='back'
                g.edge(tail_name=edge['input'], 
                        head_name=edge['output'], 
                        xlabel=XLABEL,
                        penwidth=str(0.1+abs((edge['amount'])**0.1)),
                        weight='1', #str(edge['PFD_weight']),
                        dir=direction,
                        fontcolor='white', 
                        fontsize='6', 
                        color='black', 
                        style='filled', 
                        fillcolor='white',
                        shape='ellipse',
                        #edge_attr={"weight" : str(edge['PFD_weight'])}
                        )
                
        if edge['db_input'] == 'con391':
                direction='forward'
                line_col='black'
                if edge['amount'] < 0: line_col='#8e0c0c' 
                if abs(np.log10(edge['amount'])) > 2: XLABEL="{:.2e} {}".format(edge['amount'] , edge['unit'])
                else: XLABEL="{:.2f} {}".format(edge['amount'] , edge['unit'])
                g.edge(tail_name=edge['input'], 
                        head_name=edge['output'],
                        xlabel=XLABEL,
                        penwidth='1', #str(0.1+abs((edge['amount'])**0.1)),
                        weight='1', #str(edge['PFD_weight']),
                        dir=direction,
                        minlen='2',
                        fontcolor='black', 
                        fontsize='6', 
                        color=line_col, 
                        style='filled', 
                        fillcolor='white',
                        shape='ellipse',
                        xlabelfillcolor='white',
                        # xlabeldistance='-1'

                        #edge_attr={"weight" : str(edge['PFD_weight'])}
                        )
                
        if edge['db_input'] == 'fg_'+model:
                direction='forward'
                if abs(np.log10(edge['amount'])) > 3: XLABEL="{:.1e} {}".format(edge['amount'] , edge['unit'])
                else: XLABEL="{:.2f} {}".format(edge['amount'] , edge['unit'])
                if edge['amount'] < 0: direction='back',
                g.edge(tail_name=edge['input'], 
                        head_name=edge['output'],
                        xlabel=XLABEL,
                        penwidth='1', #str(0.1+abs((edge['amount'])**0.1)),
                        weight=str(10),
                        dir=direction,
                        minlen='3',
                        fontcolor='black', 
                        fontsize='6', 
                        xlabelcolor='white', 
                        style='filled', 
                        xlabelfillcolor='white',
                        shape='ellipse',
                        # xlabeldistance='0'
                        

                        #edge_attr={"weight" : str(edge['PFD_weight'])}
                        )
        
        
    g.view()
    g.save()
    # g.render()
    # return g


        #%%

#         for edge in edges:
#              #  
#             #if edge['unit'] == 'm3': edge['unit'] = "m\u00B2" # wtf? 

#             if 'PFD_weight' not in edge:
#                 edge['PFD_weight'] = 0.1
            
#                     # change arrow direction for biosphere flows
            

#             elif act['db'] == 'con391':
#                 g.node(act['name'], label=act['name'], shape='box', color='blue', style='filled', fontcolor='white')
                

#             elif 'fg' in act['db'] :
#                 g.node(act['name'], color='red')
                
#                 if 'Succinic acid production' in act['name']:
#                     g.node(act['name'], color='pink', shape='ellipse', style='filled')

#             try: 
#                 g.node(act['name'], pos=act['PFD_pos'])
#             except KeyError:
#                 pass

#             try:
#                 g.node(act['amount'], size=act['PFD_size'])
#             except KeyError:
#                 pass
#             else:
#                 direction='forward'

#             g.edge(tail_name=edge['input'], 
#                     head_name=edge['output'], 
#                     label="{:.2f} {}".format(edge['amount'] , edge['unit']),
#                     penwidth=str(0.1+(edge['amount'])**0.1),
#                     weight=str(edge['PFD_weight']),
#                     dir=direction,
#                     #edge_attr={"weight" : str(edge['PFD_weight'])}
#                     )
            
#             g.render()
#             g
#%%
if __name__ == "__main__":
    models = ['corn', 'bread']
    for model in models: 
        nodes, edges, model = extract_nodes_edges(model)
        write_process_diagram(nodes, edges, model)