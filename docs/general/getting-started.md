# Getting Started

## Prerequisites

To run this project, you need the following dependencies:

* Python 3.9+

If you haven't installed Python and an IDE yet, [go back to the "Python 3 and IDE setup" page](setup.md).
 
## Cloning the project and installing dependencies

1. Clone the git repository:

   ``` sh
   git clone https://github.com/Tanikai/virtual-mqtt-scenario.git
   cd virtual-mqtt-scenario
   ```

2. Install required Python packages:

   ``` sh
   pip install -r requirements.txt
   ```

## Running the project

### From the command line

1. Run the project with this command:
   ``` sh
   py src/main.py
   ```
   
### VS Code

1. Open the **virtual-mqtt-scenario** directory with VS Code
2. Create a file named `launch.json` in the root directory of the project. Your
   directory structure should look like this:
   ```
   virtual-mqtt-scenario
   ├─ launch.json
   ├─ docs/
   ├─ src/
   └─ ...
   ```
3. Set the contents of the `launch.json` file to this:
   ``` json title="launch.json"
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Python: Launch main.py",
               "type": "python",
               "request": "launch",
               "program": "${workspaceFolder}/src/main.py",
               "console": "integratedTerminal",
               "justMyCode": true
           }
       ]
   }
   ```  
4. Press F5 to run the "Python: Launch main.py" configuration (debugger enabled)

!!! caution
    The `${workspaceFolder}` value refers to the root directory that is currently
    open in VS Code. If you open a different directory (e.g. the parent directory of virtual-mqtt-scenario),
    there will be an error that `main.py` cannot be found.

### PyCharm

1. In the top right corner, open the "Configurations" Listbox and click on "Edit
   Configurations"
2. Click on the + Symbol in the top left corner to add a new configuration
3. Set the "Script path" setting to the following path:
   ```
   [YOUR ABSOLUTE PATH TO THE PROJECT]/virtual-mqtt-scenario/src/main.py
   ```
4. Set the "Working Directory" setting to the following path:
   ```
   [YOUR ABSOLUTE PATH TO THE PROJECT]/virtual-mqtt-scenario/
   ```
5. Save your changes
6. Select your new configuration and run the project with Shift+F10
   
## Building the documentation

1. Install required Python packages for MkDocs:
    ``` sh
    pip install -r requirements_mkdocs.txt
    ```
   
2. Run the MkDocs server:
   ``` sh
   cd virtual-mqtt-scenario
   mkdocs serve
   ```

Now you have a live preview of the documentation website. Saved changes to the 
Markdown documentation are shown immediately.
   