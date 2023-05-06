#%%

import graphviz as gv

#%% PARAMETERS

x = 1

steam_amount_total = 40.531
water_amount_total = 0.273
elec_amount_total = 0.197
kerosene_amount_total = 0.273

bread_amount_feed_treat = x

water_amount_feed_treat = x
elec_amount_feed_treat = x
kerosene_amount_feed_treat = x
steam_amount_feed_treat = x

ecoli_amount_bac_ferm = x
steam_amount_bac_ferm = x
water_amount_bac_ferm = x
elec_amount_bac_ferm = x
kerosene_amount_bac_ferm = x
biogas_amount_bac_ferm = x

CO2_amount_unalloc_bio = x
CH4_amount_unalloc_bio = x
NH3_amount_unalloc_bio = x
NOx_amount_unalloc_bio = x
SO2_amount_unalloc_bio = x
CrVI_amount_unalloc_bio = x
As_amount_unalloc_bio = x
PAH_amount_unalloc_bio = x


#%% ADD ACTIVITIES

acts = []

# foreground activities

bread_waste = {
    'name': 'bread waste market',
    'code': 'bread_waste',
    'db' : 'foreground',
}
acts.append(bread_waste)

enz_mkt = {
    'name': 'enzyme market',
    'code': 'enz_mkt',
    'db' : 'foreground',
}
acts.append(enz_mkt)

ecoli_prop = {
    'name': 'Ecoli market',
    'code': 'ecoli_prop',
    'db' : 'foreground',
    
}
acts.append(ecoli_prop)

MgCO3_mkt = {
    'name': 'MgCO3 market',
    'code': 'MgCO3_mkt',
    'db' : 'con391',
}
acts.append(MgCO3_mkt)

feed_treat = {
    'name': 'feed pretreatment',
    'code': 'feed_treat',
    'db' : 'foreground',
    'PFD_pos': '0.25,0.5',
    'PFD_size': '5,5',
}
acts.append(feed_treat)

bact_ferm = {
    'name': 'bacterial fermentation',
    'code': 'bact_ferm',
    'db' : 'foreground',
    'PFD_pos': '0.5,0.5',
    'PFD_size': '5,5',
}
acts.append(bact_ferm)

purif = {
    'name': 'Succinic acid purification',
    'code': 'SA_purif',
    'db' : 'foreground',
    'PFD_pos': '0.75,0.5',
    'PFD_size': '5,5',
}
acts.append(purif)

sol_biomass = {
    'name': 'solid biomass market',
    'code': 'sol_biomass',
    'db' : 'foreground',
}
acts.append(sol_biomass)

SA_mkt = {
    'name': 'succinic acid market',
    'code': 'SA_mkt',
    'db' : 'foreground',
}
acts.append(SA_mkt)


# ecoinvent activities

HCl_mkt = {
    'name': 'HCl market',
    'code': 'HCl_mkt',
    'db' : 'con391',
}
acts.append(HCl_mkt)

NaCl_brine = {
    'name': 'NaCl brine x%', # find out what % is used
    'code': 'NaCl_brine',
    'db' : 'con391',
}
acts.append(NaCl_brine)

NaOH_mkt = {
    'name': 'NaOH market',
    'code': 'NaOH_mkt',
    'db' : 'con391',
}
acts.append(NaOH_mkt)

steam_mkt = {
    'name': 'steam market',
    'code': 'steam_mkt',
    'db' : 'con391'

}
acts.append(steam_mkt)

water_mkt = {
    'name': 'water market',
    'code': 'water_mkt',
    'db' : 'con391'
}
acts.append(water_mkt)

elec_mkt = {
    'name': 'electricity market',
    'code': 'elec_mkt',
    'db' : 'con391'
}
acts.append(elec_mkt)

biogas_mkt = {
    'name': 'biogas market',
    'code': 'biogas_mkt',
    'db' : 'con391'
}
acts.append(biogas_mkt)

# maybe this one is mktuced onsite
kerosene = {
    'name': 'heating oil market',
    'code': 'kerosene',
    'db' : 'con391' 
}
acts.append(kerosene)

# biosphere flows

CO2 = {
    'name': 'Carbon dioxide, fossil',
    'code': 'CO2',
    'db' : 'biosphere3',
    'type': 'emission',
}
acts.append(CO2)

CH4 = {
    'name': 'Methane, fossil',
    'code': 'CH4',
    'db' : 'biosphere3',
    'type': 'emission',
}
acts.append(CH4)

NH3 = {
    'name': 'Ammonia',
    'code': 'NH3',
    'db' : 'biosphere3',
    'type': 'emission',
}
acts.append(NH3)

NOx = {
    'name': 'Nitrogen oxides',
    'code': 'NOx',
    'db' : 'biosphere3',
    'type': 'emission',
}
acts.append(NOx)

SO2 = {
    'name': 'Sulfur dioxide',
    'code': 'SO2',
    'db' : 'biosphere3',
    'type': 'emission',
}
acts.append(SO2)

CrVI = {
    'name': 'Chromium VI',
    'code': 'CrVI',
    'db' : 'biosphere3',
    'type': 'emission',

}
acts.append(CrVI)

As = {
    'name': 'Arsenic',
    'code': 'As',
    'db' : 'biosphere3',
    'type': 'emission',
}
acts.append(As)

PAH = {
    'name': 'Polyaromatic hydrocarbons',
    'code': 'PAH',
    'db' : 'biosphere3',
    'type': 'emission',
}
acts.append(PAH)

#%% ADD EDGES

edges = []


## foreground edges

# edges to feed pretreatment

bread_wasteTOfeed_treat = {
    'from': 'bread_waste',
    'to': 'feed_treat',
    'amount': bread_amount_feed_treat, # unknown
    'unit': 'kg',
    'type': 'technosphere',
    'PFD_weight' : 3,
}
edges.append(bread_wasteTOfeed_treat)

water_mktTOfeed_treat = {
    'from': 'water_mkt',
    'to': 'feed_treat',
    'amount': water_amount_feed_treat, # unknown
    'unit': 'm3',
    'type': 'technosphere'
}
edges.append(water_mktTOfeed_treat)

elec_mktTOfeed_treat = {
    'from': 'elec_mkt',
    'to': 'feed_treat',
    'amount': elec_amount_feed_treat, # unknown
    'unit': 'kWh',
    'type': 'technosphere'
}
edges.append(elec_mktTOfeed_treat)

keroseneTOfeed_treat = {
    'from': 'kerosene',
    'to': 'feed_treat',
    'amount': kerosene_amount_feed_treat, # unknown
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(keroseneTOfeed_treat)

steam_mktTOfeed_treat = {
    'from': 'steam_mkt',
    'to': 'feed_treat',
    'amount': steam_amount_feed_treat , # unknown
    'unit': 'MJ',
    'type': 'technosphere'
}
edges.append(steam_mktTOfeed_treat)

enz_mktTOfeed_treat = {
    'from': 'enz_mkt',
    'to': 'feed_treat',
    'amount': 0.007,
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(enz_mktTOfeed_treat)

# edges to bacterial fermentation

feed_treatTObac_ferm = {
    'from': 'feed_treat',
    'to': 'bact_ferm',
    'amount': 10, # unknown
    'unit': 'kg',
    'type': 'technosphere',
    'PFD_weight' : 3,
}
edges.append(feed_treatTObac_ferm)


ecoli_propTObac_ferm = {
    'from': 'ecoli_prop',
    'to': 'bact_ferm',
    'amount': ecoli_amount_bac_ferm,  # unknown
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(ecoli_propTObac_ferm)

MgCO3_mktTObac_ferm = {
    'from': 'MgCO3_mkt',
    'to': 'bact_ferm',
    'amount': 0.273,
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(MgCO3_mktTObac_ferm)

NaOHTObac_ferm = {
    'from': 'NaOH_mkt',
    'to': 'bact_ferm',
    'amount': 0.197,
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(NaOHTObac_ferm)

# unallocated

steam_mktTObac_ferm = {
    'from': 'steam_mkt',
    'to': 'bact_ferm',
    'amount': steam_amount_bac_ferm,
    'unit': 'MJ',
    'type': 'technosphere'
}
edges.append(steam_mktTObac_ferm)

water_mktTObac_ferm = {
    'from': 'water_mkt',
    'to': 'bact_ferm',
    'amount': water_amount_bac_ferm,
    'unit': 'm3',
    'type': 'technosphere'
}
edges.append(water_mktTObac_ferm)

elec_mktTObac_ferm = {
    'from': 'elec_mkt',
    'to': 'bact_ferm',
    'amount': elec_amount_bac_ferm,
    'unit': 'kWh',
    'type': 'technosphere'
}
edges.append(elec_mktTObac_ferm)

keroseneTObac_ferm = {
    'from': 'kerosene',
    'to': 'bact_ferm',
    'amount': kerosene_amount_bac_ferm,
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(keroseneTObac_ferm)

# isn't there some ch4 captured from the fermentation process? to burn?

bac_fermTObiogas_mkt = {
    'from': 'bact_ferm',
    'to': 'biogas_mkt',
    'amount': biogas_amount_bac_ferm,
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(bac_fermTObiogas_mkt)

# edges to succinic acid purification

bac_fermTOpurif = {
    'from': 'bact_ferm',
    'to': 'SA_purif',
    'amount': x,
    'unit': 'kg',
    'type': 'technosphere',
    'PFD_weight' : 3,
}
edges.append(bac_fermTOpurif)

HCl_mktTOSA_purif = {
    'from': 'HCl_mkt',
    'to': 'SA_purif',
    'amount': 0.079,
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(HCl_mktTOSA_purif)

NaCl_brineTOSA_purif = {
    'from': 'NaCl_brine',
    'to': 'SA_purif',
    'amount': 15.007,
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(NaCl_brineTOSA_purif)


feed_treatTObac_ferm = {
    'from': 'feed_treat',
    'to': 'bact_ferm',
    'amount': 0.273,
    'unit': 'kg',
    'type': 'technosphere',
    'PFD_weight' : 3,
}
edges.append(feed_treatTObac_ferm)

# outputs

SA_purifTOsol_biomass = {
    'from': 'SA_purif',
    'to': 'sol_biomass',
    'amount': 10.639, # unknown
    'unit': 'kg',
    'type': 'technosphere'
}
edges.append(SA_purifTOsol_biomass)

SA_purifTOSA_mkt = {
    'from': 'SA_purif',
    'to': 'SA_mkt',
    'amount': 1, # unknown
    'unit': 'kg',
    'type': 'technosphere',
    'PFD_weight' : 3,
}
edges.append(SA_purifTOSA_mkt)


# unallocated biosphere3 flows

# group to one node called unallocated biosphere3 flows
# unalloc_biosphere3 = {
#     "name" : "unallocated biosphere3 flows",
#     "code" : "unalloc_bio",
#     "db" : "foreground"
# }
# acts.append(unalloc_biosphere3)

# add edges

# feed_treatTOunalloc_bio = {
#     'from': 'feed_treat',
#     'to': 'unalloc_bio',
#     'amount': 10, # unknown
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(feed_treatTOunalloc_bio)

# bact_fermTOunalloc_bio = {
#     'from': 'bact_ferm',
#     'to': 'unalloc_bio',
#     'amount': 10, # unknown
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(bact_fermTOunalloc_bio)

# SA_purifTOunalloc_bio = {
#     'from': 'SA_purif',
#     'to': 'unalloc_bio',
#     'amount': 10, # unknown
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(SA_purifTOunalloc_bio)


# unalloc_bioTOCO2 = {
#     'from': 'unalloc_bio',
#     'to': 'CO2',
#     'amount': CO2_amount_unalloc_bio,
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(unalloc_bioTOCO2)

# unalloc_bioTOCH4 = {
#     'from': 'unalloc_bio',
#     'to': 'CH4',
#     'amount': CH4_amount_unalloc_bio,
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(unalloc_bioTOCH4)

# unalloc_bioTONH3 = {
#     'from': 'unalloc_bio',
#     'to': 'NH3',
#     'amount': NH3_amount_unalloc_bio,
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(unalloc_bioTONH3)

# unalloc_bioTONOx = {
#     'from': 'unalloc_bio',
#     'to': 'NOx',
#     'amount': NOx_amount_unalloc_bio,
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(unalloc_bioTONOx)

# unalloc_bioTOSO2 = {
#     'from': 'unalloc_bio',
#     'to': 'SO2',
#     'amount': SO2_amount_unalloc_bio,
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(unalloc_bioTOSO2)

# unalloc_bioTOCrVI = {
#     'from': 'unalloc_bio',
#     'to': "CrVI",
#     'amount': CrVI_amount_unalloc_bio,
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(unalloc_bioTOCrVI)

# unalloc_bioTOAs = {
#     'from': 'unalloc_bio',
#     'to': 'As',
#     'amount': As_amount_unalloc_bio,
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(unalloc_bioTOAs)

# unalloc_bioTOPAH = {
#     'from': 'unalloc_bio',
#     'to': 'PAH',
#     'amount': PAH_amount_unalloc_bio,
#     'unit': 'kg',
#     'type': 'biosphere3'
# }
# edges.append(unalloc_bioTOPAH)

for act in acts:
    if act['db'] == 'biosphere3':
        for INPUT in acts:
            if INPUT["code"] in ['feed_treat', 'bact_ferm', 'SA_purif']:
                edge = {
                    'from': INPUT['code'],
                    'to': act['code'],
                    'amount': 1, # unknown
                    'unit': 'kg',
                    'type': 'biosphere3'
                }
                edges.append(edge)

        act['PFD_weight'] = 3

# %% Make process flow diagram



g = gv.Digraph(
                filename="SuccinicAcidmarket", 
                #engine='twopi', 
                format='svg',
                graph_attr={'rankdir':'LR',
                            'pad': '0.1',
                }) 


for act in acts:
    g.node(act['code'], label=act['name'], shape='box')
    
    if act['db'] == 'con391':
        g.node(act['code'], color='blue')
    elif act['db'] == 'foreground':
        g.node(act['code'], color='red')
    elif act['db'] == 'biosphere3':
        g.node(act['code'], color='green', label=act['code'], shape='ellipse')
    
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
        edge['PFD_weight'] = 1
    
    g.edge(tail_name=edge['from'], 
            head_name=edge['to'], 
            label=str(round(edge['amount'],2)) + ' ' + edge['unit'],
            penwidth=str(0.1+(edge['amount'])**0.5),
            weight=str(edge['PFD_weight']),
            #edge_attr={"weight" : str(edge['PFD_weight'])}
            )


g
g.render()
#g.render(neato_no_op=2)
# %% MAKE DATABASES

import bw2io as bi
import bw2data as bd

bd.projects.report()

bd.projects.set_current("cLCA-aalborg")
bd.databases

bio = bd.Database("biosphere3")
ei = bd.Database("con391")

# make foreground database

del bd.databases["foreground"]
fg = bd.Database("foreground")
fg.register()

for act in acts:
    if act['db'] == 'foreground':
        node = fg.new_node(name=act['name'], code=act['code'])
        node.save()

        for edge in edges:
                if edge['to'] == node['code']: 
                    node.new_edge(input=bd.get_node(code=edge['from']), amount=edge['amount'], type=edge['type'])
    node.save()



# %%
for a in fg:
    print(a.as_dict())
    for e in a.technosphere():
        print(e.as_dict())
    for e in a.biosphere():
        print(e.as_dict())