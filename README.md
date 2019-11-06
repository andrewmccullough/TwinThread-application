# TwinThread application

This app was built with Python and Tkinter. It offers a simple GUI for browsing the provided JSON dataset.

#### _approx. completion time 3h 45m_
GitHub post and readme.md took additional 25m.

## How to run

The script is built with Python 3 and native Python libraries (urllib, json, ssl, sys, and tkinter). The only thing required to run it is a current Python 3 installation. Download `main.py` and run it as a Python script. 

On Mac, navigate to the proper directory using Terminal and run the command `python3 main.py`. On Windows, navigate to the proper directory using Command Prompt and run the command `py main.py`.  A GUI window will open through which all functionality can be accessed. To close the application, simply click the close button.

## Features

### Search
The search feature searches for the provided query as a substring in the name, description, and ID of an asset. As such, wildcard searches can be done simply by entering the given substring -- don't bother to include an asterisk. The search is case insensitive.

### Critical items
View assets with a critical priority.

### Class browsing
Links to classes and assets are clickable, and will open the detail page for the respective item.
