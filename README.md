[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI version](https://badge.fury.io/py/cuttle.svg)](https://badge.fury.io/py/cuttle) <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/cuttlehq?style=social">
# Cuttle CLI

![alt text](/images/cuttle-logo.png)

Converting a Python notebook into a deployable project is hard and shifts the source of truth away from your initial development environment. Cuttle uses code generation to transform your notebook into deployable python projects (ex. Airflow pipeline, Flask API or just a Python script) without writing any extra code. It is built to work with tranformer plugins making it possible to support any number of output projects.

Cuttle requires creating environments for different tranformations which makes your notebook configurable by setting python variables and removes cells based on the transformation environment.

#### Getting Started

Cuttle needs to be initialized in the same folder as your notebook project. 

```
cuttle init
cuttle create sample-environment --tranformer plugin-name
cuttle transform sample-environment
```

This should create a `cuttle.json` file which can be pushed to the project git repository.

Cuttle configuration is either cell or line scoped. Cell scoped commands need to be mentioned at the top of the cell while line scoped commands are to be mentioned at the end of the line of code.

#### Disabling Cells (Cell Scoped)

Omits the code present in the cell from the output project.

```
#cuttle-environment-disable <environment>
....
```

####  Setting Configuration (Cell Scoped)

Sets configuration needed during transformation

```
#cuttle-environment-set-config <environment> <key>=<value>
...
```

#### Getting Variable Value (Line Scoped)

Sets value of variable to configuration value

```
a = 2 #cuttle-environment-get-config <environment> <key>
...
```

#### Setting Configuration Value (Line Scoped)

Sets value of configuration from variable

```
b = 2 #cuttle-environment-set-config <environment> <key>
...
```

## Transformer Plugin Documentation

[Flask API](cuttle/transform/flask/README.md)


## For Contributors


#### Building locally

```
python setup.py sdist bdist_wheel
```

#### Install using source

```
python setup.py install
```

#### Check contents of package

```
tar tzf dist/cuttle-<version>.tar.gz
```