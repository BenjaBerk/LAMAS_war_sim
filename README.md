# LAMAS War simulation implementation; group 5

## Installing requirements
To run, you have to have [graphviz](https://graphviz.org/) installed in your machine
All other requirements can be installed using the following command:
```
pip install requirements.txt
```
This will install the python Graphviz library, but
you will still need the actual Graphviz application, making sure that graphviz is added to the path of your system, see the graphviz documentation for help.
## First run
run:
```
python3 game/main.py -sv
```
-s loads up the default scenario

-v vizualizes the Kripke models

For help on running the program enter the following in the command line:

``
python3 game/main.py -h
``

Run it from the root folder to run the project

## Scenario editor
The file `scenario.py` can be changed to make the scouting rounds pre-determined with the -s flag
```
scenario = {
    "strenghts": ["weak", "strong", "strong"],
    "strategies": ["defensive","defensive","defensive"],
    "decisions": [
        [0,0, 1],
        [1,2, 0], 
    ]
}
```
The actions taken by players in a scenario can be adjusted by changing the lists under 'decisions'.
This list is build in such a way that every element describes an action, e.g. [0,0,1] means that player 3 scouts player 2.
Adding or removing players to a scenario can easily be done by extending the lists with your desired action and strength for that player.
Extra rounds can also be added simply by adding another list under the 'decision' column of the file.