# Mining-CMs-Patterns

**Mining-CMs-Patterns** is an application for mining patterns in conceptual models encoded in different conceptual modeling language. 

The current version of the application is able to parse and mine any **UML Class Diagram Model** encoded in a `{.json}` format, which can be generated through the [OntoUML](https://github.com/OntoUML/ontouml-vp-plugin) plugin for [Visual Paradigm](https://www.visual-paradigm.com/download/community.jsp) (free community edition).

The main scope of **Mining-CMs-Patterns** is to support knowledge engineers in the empirical discovery of modeling patterns. 

The application is written in **Python**, requires Python 3.6+, and has been tested on *Mac OSX*.

## Installation

- First, start by cloning this repository.
```
git clone https://github.com/unibz-core/Mining-CMs-Patterns
```

- We recommend to use `virtualenv` for development.

- Once the virtual environment is created, install the python dependencies on the virtual environment.
```
pip install -r requirements.txt
```

- Access the application folder.
```
cd scripts
```

- Start the application.
```
python3 main.py
```

## Get Started with Mining-CMs-Patterns

- Interact with the command line by providing the required inputs, e.g.:
```
Welcome to our pattern discovery application!
Press Enter to continue...
Please, select the weight of generalization relations,
('integer' from 0 to 9): 1
Please, select the weight of associations,
('integer' from 0 to 9): 3
Enter the reference number of nodes for generating graph partitions
(value ≥ 3 suggested): 5   
```
- Remember to put the models to be mined in the `models` folder.
- All the files we used in the experiment, currently collected in the `models` folder, where generated by pulling the [OntoUML Repository](https://github.com/unibz-core/ontouml-models) files in the folder `importing/ontouml-models-master/`. All the files can be renamed and extracted in a single folder by running the `fileimport.py` script.
- The output of the mining process will be created in the `output` folder.
- If you want to restart the process remember to delete all the created files through the related command.

```
Want to clear folders? (Y/N): Yes!
```
### Papers

The paper about the application and related approach was submitted at ER2022.




