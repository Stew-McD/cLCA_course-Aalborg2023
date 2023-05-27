
#%%

import bw2io as bi
import bw2data as bd

bi.__version__
bd.__version__

# %%

bd.projects.set_current("cLCA-aalborg")
bd.projects.report()

bd.databases

bi.bw2setup()

db_name = "con391"
con_path = "/home/stew/CML/coding/DBs/EI/con391/datasets"

ei = bi.SingleOutputEcospold2Importer(con_path, db_name)

ei.apply_strategies()
ei.statistics()
ei.write_database()
db = bd.Database(db_name)
db.metadata
