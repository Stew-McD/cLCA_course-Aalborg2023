#%%
import bw2data as bd
import os
import bw2io as bi


#%% backup the project directory
os.environ["HOME"] = os.getcwd()

bi.backup.backup_project_directory("cLCA-aalborg")
# %%
backup = "brightway2-project-cLCA-aalborg-backup.16-May-2023-02-48PM.tar.gz"
bi.restore_project_directory(backup)