"""
# Brightway25: Backup and Restore Projects
## Author: Stew-McD
## Date: 27/05/2023

This Python script provides functionality for backing up and restoring a Brightway2 project directory.

## Requirements

- Python 3.x
- `bw2data` and `bw2io` packages

## Usage

1. Clone or download the `backup_and_restore_project.py` script.
2. Open the script in a Python IDE or text editor.
3. Set the following variables to the project name, whether you want to backup or restore, the directory locations and the file name:
   - `project_name`
   - `backup`
   - `restore`
   - `delete_project`
   - `custom_project_dir`
   - `project_archive`
4. Run the script.

## Notes

- The script sets the environment variable to the current directory so that the backup is saved here.
- If you have/want a custom location for the bw2 project directory, set it in the `custom_project_dir` variable.
- The backup file is saved with the name: `brightway2-project-<project_name>-backup.<date-time>.tar.gz`.
- If the project already exists and you want to delete it before restoring, set the `delete_project` variable to `True`.
- If you want to change the backup file name, change the `project_archive` variable.
- The script was tested with Brightway2 version 3.7.2.

"""


import os
import bw2data as bd
import bw2io as bi

# Print script information
print("="*50)
print("Brightway2 Backup and Restore Projects")
print("="*50)
print("This Python script provides functionality for backing up and restoring a Brightway2 project directory.")
print("Author: Stew-McD")
print("Date: 27/05/2023\n")

# Set the following variables to the project name, whether you want to backup or restore, the directory locations and the file name
project_name = "cLCA-aalborg"
backup = False
restore = True
delete_project = True
custom_project_dir = False
project_archive = "brightway2-project-cLCA-aalborg-backup.31-May-2023-07-22PM.tar.gz"  # Change file name

# Set the environment variable to the current directory so that the backup is saved here
os.environ["HOME"] = os.getcwd()

# If you have/want want a custom location for the bw2 project directory, set it here
if custom_project_dir:
    os.environ["BRIGHTWAY2_DIR"] = os.path.join(os.environ["HOME"], "bw2_projects")

# Backup the project directory
if backup:
    print(f"\nBacking up {project_name} to {os.getcwd()}...")
    bi.backup_project_directory(project_name)
    print("Backup complete.")

# Restore the project directory
# File is saved with the name: brightway2-project-<project_name>-backup.<date-time>.tar.gz
if restore:
    print(f"\nRestoring {project_archive}...")
    try:
        bi.restore_project_directory(project_archive,overwrite_existing=True)
        print("Restore complete.")
    except AssertionError:
        print("Project archive not found. Please check file name and location.")
    except ValueError: 
        print("Project already exists. Please delete or rename it first.")
        if delete_project: 
            bd.projects.delete_project(project_name, delete_dir=True)
            print(f'Deleted {project_name}. Restoring {project_archive}...')
            bi.restore_project_directory(project_archive)
            print("Restore complete.")
    except Exception as e:
        print("Something went wrong. Please check the error message below.")
        print(e)

