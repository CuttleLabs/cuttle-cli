# Flask Transformer Plugin for Cuttle

Enables converting a Jupyter Notebook to a Flask API project using [Cuttle](https://github.com/CuttleLabs/cuttle-cli). The plugin works by converting a code cell into function attached to a Flask route ([Check Flask Project Layout](https://flask.palletsprojects.com/en/2.0.x/tutorial/layout/)).

## Add required cell scoped configuration

Required config - route, method, response

```
#cuttle-environment-set-config <environment> route=<route> method=<http method> response=<response variable>
....
```

## Fetch data from request object

The plugin provides the original `request` object provided by Flask ([properties](https://flask.palletsprojects.com/en/2.0.x/api/?highlight=request#flask.Request)). This can be used along with Cuttle line scoped get config. 

Example:

```
file = open("./images/mnist3.png", "rb") #cuttle-environment-assign mnist-api request.files['file']
```

This results in:

```
file = request.files['file']
```


[MNIST API Example Project](https://github.com/CuttleLabs/cuttle-cli/tree/master/examples/mnist-api)