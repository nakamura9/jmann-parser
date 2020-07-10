# JMann parser

---

### Description

The Jmann parser is designed to parse the options defined in prod_types.xlsx and 
break them down into symbols that can be used to filter products in a very large 
list of products.

The breakdown is stored in the text and json files that come with this project

### Installation 

- clone project
- create and activate a virtual environment
- cd into project root
- install the project requirements 
    ` pip install -r requirements.txt `


run project using:
**On Windows** 
```
$env:FLASK_APP = "server.py" 
$env:FLASK_ENV = "development"
python -m flask run
```
**On Linux**
```
$ export FLASK_APP="server.py"
$ flask run
```
- Visit localhost:5000 to navigate through the products via multi tier search