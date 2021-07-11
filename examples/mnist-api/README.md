# Mnist API

This directory contains the files needed to transform your notebook into an API.

* `cuttle.json` contains the configuration used by the transformer. Use command `cuttle init` to create this. Refer main README for further details about this file.
* `mnist.ipynb` is the notebook we're going to transform.
* The images folder consists of labelled images to train our model.

After transforming the notebook into an API, the `output` folder is created with a sub-directory containing the name of the environment. This folder consists the `main.py`.

For reference, this is how the transformed file looks like:
https://gist.github.com/668b811cf5a5be6ada42176d6736faee.git
