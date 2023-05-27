# Consequential Life Cycle Assessment Course
##  Aalborg University - May '23

This repository contains the code for the cLCA group project at Aalborg University.

The course files are in the folder 'moodle'

See the interactive notebook main.ipynb to view the code and results from a previous run.


# Contents
* Usage
* Code explanation
* Setup
* Contributing

# Usage:
1. install requirements: `pip install -r requirements.txt`
3. if you don't have ecoinvent installed, download it and run import_ecoinvent.py
4. configure main.py and run it

# Code explanation

## main.py
### * Importing Modules

The code begins by importing several modules, including `os`, `sys`, and `shutil` for general file operations, `bw2calc`, `bw2data`, and `bw2io` for life cycle assessment calculations and data management, and `seaborn` for data visualization.
Additionally, there are imports from custom modules (`visualisation`, `add_uncertainties`, `import_db_from_file`, `LCA_calculations`, and `make_process_diagram`) that contain specific functions used later in the code.

### * Setting Up Models

The code initializes a list called `models` and appends two models, "bread" and "corn", to it.

### * Setting Flags

The code sets several Boolean flags (`remove`, `rebuild`, `recalculate`, `recalculate_MC`, `revisualise`) to control the execution of specific functions later in the code.

### * Removing Old Results Folder

If the `remove` flag is `True` and a folder named "results" exists, the code removes the folder and its contents using the `shutil.rmtree` function.

### * Setting Parameters for Monte Carlo Analysis

The code sets various parameters for the Monte Carlo analysis, such as the number of iterations (`iterations`), scale percent (`scale_percent`), and distribution ID (`dist_id`). The distribution ID determines the type of probability distribution used for uncertainty analysis.

### * Setting Scenarios

The code defines a dictionary called `scenarios` that represents different LCA scenarios. Each scenario is associated with a Boolean value indicating whether it should be applied.
The scenarios include "CoproductsToWaste", "EnergyEfficient", "WaterEfficient", and "CoproductsToLowerMarket". Each scenario modifies specific aspects of the LCA model.

### * Writing Databases, Adding Uncertainties, Inspecting, and Exporting

If the `rebuild` flag is `True`, the code iterates over each model and performs the following steps:
- Writes the database for the model using the `write_database` function from the custom module `import_db_from_file`.
- Adds uncertainties to the database using the `add_uncertainties` function from the custom module `add_uncertainties`.
- Inspects the database using the `inspect_db` function from the custom module `import_db_from_file`.
- Exports the database using the `export_db` function from the custom module `import_db_from_file`.
- If the `redo_diagrams` flag is `True`, it extracts nodes and edges from the model using the `extract_nodes_edges` function from the custom module `make_process_diagram` and generates a process diagram using the `write_process_diagram` function from the same module.

### * Loading the Database

The code loads the functional unit process ("fg") from the database of the current model (`f'fg_{model}'`) using the `bd.Database` function from `bw2data`.

### * Setting up Scenarios

For each model, the code iterates over the scenarios and performs specific modifications to the LCA model based on the active scenarios.

### * Extracting Nodes and Edges, Writing Process Diagrams

After modifying the LCA model based on scenarios, the code extracts nodes and edges from the model using the `extract_nodes_edges` function from the custom module `make_process_diagram`.
It then writes a process diagram based on the extracted nodes, edges, model, and scenario name using the `write_process_diagram` function from the same module.

### * Recalculating LCA Scores

If the `recalculate` flag is `True`, the code iterates over each model and performs the following steps:
- Calculates the LCA scores for the model and scenario using the `get_LCA_scores` function from the custom module `LCA_calculations`.
- Generates an LCA report for the model and scenario using the `get_LCA_report` function from the same module.

### * Calculating Monte Carlo Results

If the `recalculate_MC` flag is `True`, the code iterates over each model and performs the following steps:
- Calculates the single LCA score for the model and scenario using the `get_LCA_scores` function from the custom module `LCA_calculations`.
- Performs Monte Carlo analysis by calling the `get_MCLCA_scores` function from the same module, passing the single score, number of iterations, Monte Carlo type, and scenario name.

### * Plotting Monte Carlo Results and Statistical Tests

If the `revisualise` flag is `True`, the code imports the `plot_MC_results` function from the custom module `visualisation`.
It plots the Monte Carlo results using the `plot_MC_results` function, passing the Monte Carlo type and scenario name.
Additionally, it performs statistical tests and displays the results using the `describe` and `to_dict` functions on a DataFrame.

### * STATS_ARRAYS DISTRIBUTION IDS

The code includes a comment listing the distribution IDs used in the `add_uncertainties` function.
These IDs correspond to different probability distributions used for uncertainty analysis in the `stats_arrays` package.

The code performs various operations related to LCA, including building and modifying LCA models, adding uncertainties, calculating LCA scores, performing Monte Carlo analysis, visualizing results, and conducting statistical tests.


## add_uncertainties.py

### * Add Uncertainties to Model Exchanges

The code block defines a function named `add_uncertainties` that adds uncertainties to the exchanges in a given model's database. The function takes three parameters: `model`, `dist_id`, and `scale_percent`.

The function performs the following steps:

- Loads the database for the specified model using the `bw2data` package.
- Iterates over each node (activity) in the database.
- Within the nested loop, iterates over each exchange of the current node.
- Sets the `uncertainty type` of the exchange to the provided `dist_id`.
- Calculates the `loc` (location parameter) of the uncertainty based on the exchange's amount.
- Calculates the `scale` (scale parameter) of the uncertainty based on the exchange's amount and the provided `scale_percent`.
- Checks the `dist_id` to determine the distribution type and adjusts the `loc` and `scale` accordingly.
- Sets the `negative` attribute of the exchange to indicate if the amount is negative or not.
- Checks if the amount is zero and adjusts the `uncertainty type` and `loc` accordingly.
- Saves the changes made to the exchange.

### * STATS_ARRAYS Distribution IDs

The code block includes a comment listing the distribution IDs used in the `add_uncertainties` function. These IDs correspond to different probability distributions available in the `stats_arrays` package for uncertainty analysis.

The distribution IDs and their corresponding distributions are as follows:

- 0: UndefinedUncertainty
- 1: NoUncertainty
- 2: LognormalUncertainty
- 3: NormalUncertainty
- 4: UniformUncertainty
- 5: TriangularUncertainty
- 6: BernoulliUncertainty
- 7: DiscreteUniform
- 8: WeibullUncertainty
- 9: GammaUncertainty
- 10: BetaUncertainty
- 11: GeneralizedExtremeValueUncertainty
- 12: StudentsTUncertainty



## import_db_from_file.py

### * Define custom function to convert the dataframe into a set of dictionaries
This code block defines a custom function named `lci_to_bw2` that converts a pandas DataFrame into a set of dictionaries suitable for the bw2io package to create a life cycle inventory database in Brightway2.

The function takes a DataFrame (`db_df`) as input and performs the following steps:

- Extracts the activity and exchange keys from the DataFrame columns.
- Defines three nested functions: `exc_to_dict`, `act_to_dict`, and `bio_to_dict`.
  - `exc_to_dict` converts exchange data from the DataFrame into a dictionary format and appends it to a given list (`some_list`).
  - `act_to_dict` converts activity data from the DataFrame into a dictionary format.
  - `bio_to_dict` converts biosphere data from the DataFrame into a dictionary format.
- Initializes empty lists (`db_keys` and `db_values`) to store the keys and values of the final database.
- Iterates over unique activity codes in the DataFrame:
  - Selects rows corresponding to the current activity.
  - Extracts the necessary data and calls the appropriate nested function (`act_to_dict` or `bio_to_dict`) based on the activity type.
  - Appends the resulting dictionary to `db_values`.
- Combines the keys and values into a final dictionary (`bw2_db`).
- Returns the final dictionary.

### * Write database function
This code block defines a function named `write_database` that writes a life cycle inventory database for a given model.

The function takes a model name as input and performs the following steps:

- Reads the data from an Excel file corresponding to the model.
- Calls the `lci_to_bw2` function to convert the data into a dictionary format suitable for the bw2io package.
- Deletes the existing database if it already exists.
- Writes the new database to the project using the bw2io package.
- Returns the loaded database as a dictionary (`fg_dict`).

### * Inspect the database function
This code block defines a function named `inspect_db` that inspects the contents of the life cycle inventory database for a given model.

The function takes a model name as input and performs the following steps:

- Retrieves the database for the model.
- Iterates over each activity in the database.
- Prints information about each activity, including its name, unit, code, and exchanges (technosphere and biosphere).

### * Export the database function
This code block defines a function named `export_db` that exports the life cycle inventory database for a given model to an Excel file.

The function takes a model name as input and performs the following steps:

- Defines the name of the database (`db`) based on the model name.
- Uses the bw2io package to write the database to an Excel file in the specified directory.


## make_process_diagram.py
### * Extract Nodes and Edges from Model

The code block defines a function named `extract_nodes_edges` that takes a `model` as input and extracts the nodes and edges from the specified model's database. The function performs the following steps:

- Imports the required packages: `bw2data` as `bd` for accessing life cycle inventory databases.
- Sets the database name based on the input `model`.
- Loads the project and defines the databases using the `bw2data` package.
- Initializes empty lists to store the edges and nodes.
- Iterates over each activity (`act`) in the database.
- Within the nested loop, iterates over each exchange (`ex`) of the current activity.
- Extracts the necessary information from the exchange and input/output nodes.
- Creates an edge dictionary with attributes such as input name, output name, amount, unit, type, database input, database output, and PFD weight.
- Appends the edge dictionary to the `edges` list.
- After the nested loop, iterates over each edge in the `edges` list.
- Creates a node dictionary with attributes such as name, database, and type.
- Checks if the node dictionary is already in the `nodes` list to avoid duplicates.
- If the node is not already in the `nodes` list, appends the node dictionary to the `nodes` list.
- Returns the `nodes`, `edges`, and `model` variables.

### * Write Process Diagram

The code block defines a function named `write_process_diagram` that takes `nodes`, `edges`, `model`, and `scenario_name` as inputs and generates a process diagram using the `graphviz` package. The function performs the following steps:

- Imports the required packages: `graphviz` as `gv` for creating the graph object and `numpy` as `np` for numerical operations.
- Initializes a `None` value for the graph object.
- Creates a new `Digraph` object with the specified filename, engine, format, and graph attributes.
- Defines a cluster for the background flows using the `subgraph` method.
- Iterates over each node in the `nodes` list.
- Checks if the node's database is `'con391'` (technosphere flows).
- Adds the node to the background cluster with specific attributes such as font name, fill color, label, shape, style, and font color.
- Defines another cluster for the foreground flows using the `subgraph` method.
- Sets attributes for the foreground cluster such as label, margin, label location, font size, font name, style, font color, fill color, alpha, shape, and rank.
- Iterates over each node in the `nodes` list again.
- Checks if the node's database name contains `'fg'` (foreground flows).
- Adds the node to the foreground cluster with specific attributes such as label, shape, style, font name, font color, alpha, and fill color.
- Further customizes certain nodes based on their name.
- Defines a cluster for the biosphere flows using the `subgraph` method.
- Iterates over each node in the `nodes` list again.
- Checks if the node's database is `'biosphere3'`.
- Adds the node to the biosphere cluster with specific attributes such as fill color, label, shape, style, and font color.
- Iterates over each edge in the `edges` list.
- Checks the database input of the edge.
- If the database input is `'biosphere3'`, sets the direction of the edge to `'back'` and sets attributes such as ...


## LCA_calculations.py


The following code performs a Life Cycle Assessment (LCA) calculation. It imports necessary packages, sets the project, defines functions for LCA reporting, LCA scores, and Monte Carlo LCA scores. Here's a breakdown of the code:

### * Importing Packages

- `bw2data`: Importing the package as `bd`
- `bw2calc`: Importing the package as `bc`
- `seaborn`: Importing the package as `sb`
- `bw2analyzer`: Importing the package as `ba`
- `ContributionAnalysis`: Importing the class as `ca`
- `bw_processing`: Importing the package as `bwp`
- `matrix_utils`: Importing the package as `mu`
- `numpy`: Importing the package as `np`
- `pandas`: Importing the package as `pd`
- `os`
- `uncertainty_choices` from `stats_arrays`

### * Set the Project

The code sets the current project as 'cLCA-aalborg' and creates a 'results' directory if it doesn't exist.

### * Function: `get_LCA_report(model, scenario_name)`

This function generates an LCA report for the given model and scenario. Here are the main steps:

1. Get the necessary data from the database and define the functional unit (FU).
2. Define the LCA method.
3. Perform LCA calculations using `bc.LCA` with the specified demand, method, and distributions settings.
4. Generate various reports:
   - `recursive_calculation`: Writes a recursive calculation report to a CSV file.
   - `recursive_supply_chain`: Writes a recursive supply chain report to a CSV file.
   - `top_emissions`: Writes a report of top emissions to a CSV file.
   - `top_processes`: Writes a report of top processes to a CSV file.
5. Print the LCA score and write the results to a file.

### * Function: `get_LCA_scores(model, scenario_name)`

This function calculates LCA scores for the given model and scenario. Here are the main steps:

1. Get the necessary data from the database and define the functional unit (FU).
2. Search for the exchanges of the functional unit and print them.
3. Define the LCA method.
4. Perform LCA calculations using `bc.LCA` with the specified demand, method, and distributions settings.
5. Print the LCA score and write the results to a file.

### * Function: `get_MCLCA_scores(model, single_score, iterations, mc_type, scenario_name)`

This function performs Monte Carlo LCA calculations for the given model, single score, iterations, Monte Carlo type, and scenario. Here are the main steps:

1. Get the necessary data from the database and define the functional unit (FU).
2. Define the LCA method.
3. Perform LCA calculations using `bc.LCA` with the specified demand, method, and distributions settings.
4. Perform Monte Carlo simulations and store the results in a DataFrame.
5. Plot a scatter plot of Monte Carlo results and save it as an image.
6. Print the Monte Carlo LCA score statistics and write the results to a file.

The code also appends the Monte Carlo results to a CSV file.

## visualization.py

### * Importing Packages

The code imports the following packages:

- `pandas` as `pd`: Used for data manipulation and analysis.
- `seaborn` as `sns`: Used for data visualization.
- `matplotlib.pyplot` as `plt`: Used for creating plots.
- `matplotlib.patheffects`: Used for adding effects to text in the plot.
- `uncertainty_choices` from `stats_arrays`: Used for defining uncertainty types.
- `os`: Used for working with file paths and directories.
- `palettable.wesanderson` as `wa`: Used for setting the color palette.

### * Function: `plot_MC_results(mc_type, scenario_name)`

This function reads the Monte Carlo results from a CSV file, plots the distributions, performs statistical tests, and saves the plot. Here are the main steps:

1. Read the CSV file into a DataFrame using the provided `mc_type` and `scenario_name` parameters.
2. Extract the uncertainty type from the CSV file name.
3. Set the color palette using the `wa.GrandBudapest4_5` palette.
4. Create a figure and axis for the plot.
5. Iterate over the columns in the DataFrame and create a histogram with density curve for each column.
6. Calculate the mean, standard deviation, minimum, and maximum for each column and annotate the plot with these statistics.
7. Perform statistical tests (Welch's t-test, Mann-Whitney U test, and Kolmogorov-Smirnov test) between the distributions.
8. Add legends, labels, and title to the plot.
9. Save the plot as an SVG image and close the plot.
10. Return the DataFrame containing the Monte Carlo results.


# cLCA-Aalborg

This repository contains the code for the cLCA group project at Aalborg University.

The course files are in the folder 'moodle'



## Setup for VSCode, GitHub CLI, Python, and pip: 

### GitHub CLI, Repository, VSCode and Python Virtual Environment with pip

This guide provides instructions for:
* installing GitHub CLI
* logging into GitHub via the terminal
* creating a directory for GitHub repositories 
* cloning a specific repository 
* setting up a virtual environment
* installing dependencies using pip 
* installing additional modules 
* and integrating with Visual Studio Code (VSCode)  


### Install GitHub CLI and clone the repository

#### Linux
```bash
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
sudo apt-add-repository https://cli.github.com/packages
sudo apt update
sudo apt install gh
```
#### MacOS
https://cli.github.com/ or... 

> brew install gh

#### Windows
https://cli.github.com/

#### Login to github
> gh auth login

#### Create a directory for GitHub repositories
> mkdir <directory>
> cd <directory>

#### Clone this repository
> gh repo clone https://github.com/Stew-McD/cLCA-Aalborg
> cd cLCA-Aalborg

### Create a virtual environment
>python3 -m venv cLCA-Aalborg

#### Activate the venv
Linux/MacOS
>source cLCA-Aalborg/bin/activate 
Windows
>cLCA-Aalborg\Scripts\activate

#### Install dependencies
> pip install -c cmutel -r requirements.txt

#### Install additional modules
> pip install <module>

#### List installed modules
> pip list

#### Deactivate the venv (if you want to leave the venv)
> deactivate


#### Integrate with VSCode

First install vscode
https://code.visualstudio.com/

To configure Visual Studio Code (VSCode) to recognize and use virtual environments, you can follow these steps:

1. Open VSCode.

2. Open the command palette by pressing Ctrl + Shift + P (Windows/Linux) or Cmd + Shift + P (macOS).

3. Type "Python: Select Interpreter" in the command palette and select it. This command allows you to choose the Python interpreter for your project.

4. If you already have a virtual environment created, you should see it listed in the dropdown menu along with other Python interpreters. Select the desired virtual environment from the list.

5. If you don't have a virtual environment created or the desired one is not listed, choose the "Enter interpreter path" option.

6. In the text box, enter the path to the Python interpreter within your virtual environment. This path will typically be in the venv or env folder within your project directory. For example, it might look like:

    Windows: <path\to\myenv>\Scripts\python.exe
    macOS/Linux: <path/to/myenv>/bin/python
    After entering the interpreter path, VSCode will use that virtual environment for the current workspace.

Now, when you work on a project within that workspace, VSCode will automatically use the specified virtual environment. You can verify this by opening a terminal within VSCode (Ctrl + backtick ```) and running python --version or pip list to see that the packages installed in the virtual environment are being used.

## Contributing

If you want to change something in the code, you can do that in vs code, then commit the changes and push them to the repository.








