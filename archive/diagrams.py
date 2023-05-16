
#%% 
from schemdraw import flow
from schemdraw import Drawing

#%%

d = Drawing()
d.config(fontsize=12, 
    font='Arial', 
    unit=1, 
    lw=1.2, 
    color='black', 
    fill='none',
)


d += flow.Arrow()
d += flow.Arrow()
d += flow.Arrow()

d += flow.Process()


d
# %%

d