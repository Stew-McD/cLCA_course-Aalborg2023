g = gv.Digraph(
                filename="SuccinicAcidmarket", 
                #engine='twopi', 
                format='svg',
                graph_attr={'rankdir':'LR',
                            'pad': '0.1',
                }) 

acts = 
for act in acts:
    g.node(act['code'], label=act['name'], shape='box')
    
    if act['db'] == 'con391':
        g.node(act['code'], color='blue')
    elif act['db'] == 'foreground':
        g.node(act['code'], color='red')
    elif act['db'] == 'biosphere3':
        g.node(act['code'], color='green', label=act['code'], shape='ellipse', style='filled', fontcolor='white',
        )
    
    if act['code'] == 'SA_mkt':
        g.node(act['code'], color='pink', shape='ellipse', style='filled')

    try: 
        g.node(act['code'], pos=act['PFD_pos'])
    except KeyError:
        pass

    try:
        g.node(act['size'], size=act['PFD_size'])
    except KeyError:
        pass


for edge in edges:
    if edge['unit'] == 'm3': edge['unit'] = 'm³' #  
    #if edge['unit'] == 'm3': edge['unit'] = "m\u00B2" # wtf? 

    if 'PFD_weight' not in edge:
        edge['PFD_weight'] = 0
    
    g.edge(tail_name=edge['from'], 
            head_name=edge['to'], 
            label=str(round(edge['amount'],2)) + ' ' + edge['unit'],
            penwidth=str(0.1+(edge['amount'])**0.5),
            weight=str(edge['PFD_weight']),
            #edge_attr={"weight" : str(edge['PFD_weight'])}
            )


g.render()