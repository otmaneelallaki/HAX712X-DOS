![](https://github.com/otmaneelallaki/HAX712X-DOS/blob/main/Beamer/carte_de_france.png=100x20)


# README


## Authors

You can reach the authors at the following addresses: <br/>
Otmane El Allaki otmane.el-allaki@etu.umontpellier.fr <br/>
Sofiane Aoues  sofiane.aoues@etu.umontpellier.fr <br/>
David Czarnecki  david.dzarnecki@etu.umontpellier.fr

## Introduction : 
This project aims to : <br/>

-Create  a python package allowing any user to predict for a desired day different sources of energy consumption in France. <br/>
-Display a geographical map to describe the energy consumption of cities of France.

## Installation : 
All the necessary packages are available at `requirements.txt` file in the source directory.
<br/>

Data source :  (https://odre.opendatasoft.com/explore/dataset/eco2mix-national-tr/information/?disjunctive.nature&sort=-date_heure)
## Project : 
The executable python files for both of the prediction and visualization are available on `/Project`.
## ClassModel : 
Our main model is availabe on ` ./Project/ClassModel.py`which contains the classes and functions used for fitting the model, you will find more details on documentation file .
## Data Collection : 
The Data Collection is available at ` ./Project/DataCollection.py `.
## Data Visualization : 
Some images and additional graphics are available at ` ./Project/Visualization.py` . 
## Documentation : 
The documentation of this package is available  at `docs/_build//html/index.html` .
## Structure : 
The `./report` folder contains a jupyter notebook to display different elements like images and data collection.
## Test : 
Tests functions are implemented in the `Test/test_Project.py` in order to assure the good development of this package.
## Beamer : 
The project will be presented in the form of an oral presentation and an explanatory beamer that will accompany our presentation, you'll find our presentation in `/Beamer` folder.

## Thanks

The authors thanks Joseph Salmon (https://github.com/josephsalmon) and Benjamin Charlier (https://github.com/bcharlier) who supervised the project.
