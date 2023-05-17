#%%

import pymrio
import pandas as pd

#%% test
test_mrio = pymrio.load_test()

print(test_mrio.get_sectors())
print(test_mrio.get_regions())

test_mrio.Z
test_mrio.emissions.F
# %% Autodownload exiobase

# exio3_folder = "/tmp/mrios/autodownload/EXIO3"
# # Download the Exiobase 3 database for the year 2011 and 2012. Save the database to the exio3_folder.
# exio_downloadlog = pymrio.download_exiobase3(storage_folder=exio3_folder, system="pxp", years=[2011, 2012])
# print(exio_downloadlog)

#%% Parse exiobase

exio3 = pymrio.parse_exiobase3(path='/tmp/mrios/autodownload/EXIO3/IOT_2012_pxp.zip')

#%% Explore exiobase
e = exio3

e.meta

sectors = e.get_sectors().to_frame()
print(list(sectors))
len(sectors)
regions = e.get_regions()
len(regions)
print(list(regions))
extensions = list(e.get_extensions())
extensions

e.calc_all()
list(e.impacts.get_rows())
#%% visualise

import matplotlib.pyplot as plt

plt.figure(figsize=(15,15))
plt.imshow(e.A, vmax=1E-3)
plt.xlabel('Countries - sectors')
plt.ylabel('Countries - sectors')
plt.show()

#%%

print(e.impacts.unit.loc['Nitrogen'])
e.impacts.D_cba_reg.loc['Nitrogen']

#%%

with plt.style.context('ggplot'):
    e.impacts.plot_account(['Nitrogen'], figsize=(15,10))
    plt.show()


#%%

e.meta
charact_table = pd.read_csv(
    (PYMRIO_PATH["test_mrio"] / Path("concordance") / "emissions_charact.tsv"),
    sep="\t",
)
charact_table

#%%

list(e.get_extensions())

e.Z
e.Y
e.x
e.A
e.L
e.impacts.D_cba_reg
e.impacts.D_cba_reg.loc['Nitrogen']

e.impacts.D_pba_reg.loc['Nitrogen']
