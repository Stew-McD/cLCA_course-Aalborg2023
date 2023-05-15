# cLCA-Aalborg

This repository contains the code for the cLCA group project at Aalborg University.

## Contents
* Setup
* Usage
* Contributing

## Setup: 

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


### Install GitHub CLI

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

#### Create a virtual environment
>python3 -m venv cLCA-Aalborg

#### Activate the venv
Linux/MacOS
>source cLCA-Aalborg/bin/activate 
Windows
>cLCA-Aalborg\Scripts\activate

#### Instal dependencies
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

    Windows: path\to\myenv\Scripts\python.exe
    macOS/Linux: path/to/myenv/bin/python
    After entering the interpreter path, VSCode will use that virtual environment for the current workspace.

Now, when you work on a project within that workspace, VSCode will automatically use the specified virtual environment. You can verify this by opening a terminal within VSCode (Ctrl + backtick ```) and running python --version or pip list to see that the packages installed in the virtual environment are being used.









