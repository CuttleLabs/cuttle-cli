![alt text](/images/cuttle-logo.png)

# Cuttle CLI

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![PyPI version](https://badge.fury.io/py/cuttle.svg)](https://badge.fury.io/py/cuttle) <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/cuttlehq?style=social"> ![Unit Tests](https://github.com/CuttleLabs/cuttle-cli/actions/workflows/test.yml/badge.svg) [![Downloads](https://pepy.tech/badge/cuttle/week)](https://pepy.tech/project/cuttle)

Converting a Python notebook into a deployable project is hard and shifts the source of truth away from your initial development environment. Cuttle uses code generation to automate transformation of your notebook into deployable python projects (ex. Airflow pipeline, Flask API or just a Python script) without writing any extra code. 

## 😎 Features

* Tranformer plugins making it possible to support any number of output projects.
* Environment support to allow different configurations and transformations for the same notebook.
* Easy to integrate into your Dev Ops pipeline.

## 🚀 Getting Started

Cuttle needs to be initialized in the same folder as your notebook project. 

```
cuttle init
cuttle create <new environment name> --transformer <plugin-name>
```

This should create a `cuttle.json` file which can be pushed to the project git repository.

Cuttle configuration is either cell or line scoped. Cell scoped commands need to be mentioned at the top of the cell while line scoped commands are to be mentioned at the end of the line of code.

### Cell Scoped Configuration

#### Disabling Cells

Omits the code present in the cell from the output project.

```
#cuttle-environment-disable <environment>
....
```

####  Setting Configuration

Sets configuration needed during transformation. Check transformer documentation for possible keys.

```
#cuttle-environment-set-config <environment> <key>=<value>
...
```

### Line Scoped Configuration

#### Getting Variable Value

Sets value of variable to global environment configuration value in `cuttle.json`

```
a = 2 #cuttle-environment-get-config <environment> <key>
...
```

#### Assign Transformer Provided Dependency

Sets value of variable to dependency provided by transformer. Check transformer documentation for available dependencies.

```
a = 2 #cuttle-environment-assign <environment> <dependency>
...
```

### Transform

Creates transformed project in `output` folder.

```
cuttle transform <environment>
```

## 🤓 Transformer Plugin Documentation

[Flask API](cuttle/transform/flask/README.md)


## ⭐ For Contributors


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
