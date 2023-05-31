
#%%
from py7zr import SevenZipFile
import os
import bw2io as bi
import bw2data as bd

bi.__version__
bd.__version__

# %%
bd.projects.delete_project("cLCA-aalborg", True)
bd.projects.set_current("cLCA-aalborg")
# bd.projects.report()

bd.databases

bi.bw2setup()




db_file = "con391.7z"
db_name = "con391"
tmp = "tmp/"
con_path = os.path.join(os.getcwd(),tmp, "datasets")


if not os.path.isdir(tmp):
    os.mkdir(tmp)

print("\nExtracting database...")
with SevenZipFile(db_file, 'r') as archive:
    archive.extractall(path=tmp)
    print("Extraction complete.")

ei = bi.SingleOutputEcospold2Importer(con_path, db_name)

ei.apply_strategies()
ei.statistics()
ei.write_database()
db = bd.Database(db_name)
db.metadata

