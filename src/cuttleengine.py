import json
import os
import nbformat

class CuttleEngine:
    def __init__(self):
        self.config_file_name = 'cuttle.json'

        config_file = open(self.config_file_name, "r")
        config_string = config_file.read()

        self.config = json.loads(config_string)

    def setHomePath(self, path):
        self.home_path = path

    def getEnvironments(self):
        return self.config['environments'].keys()

    def transform(self, env_name):
        plugin_path = os.path.join('plugin', self.config['environments'][env_name]['transformer'], 'main.py')
        notebook_path = os.path.join(self.home_path, 'test.ipynb')

        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)

        nb = self.envtransform(self.config, nb, 'k')

        ns = {
            'notebook': nb
        }

        with open(plugin_path) as f:
            code = compile(f.read(), plugin_path, 'exec')
            eval(code, ns, ns)

        return ns['cli']

    def envtransform(self, config, notebook, env_name):
        cells = notebook.cells
        cells_new = []

        for cell in cells:
            if cell['cell_type'] != 'code':
                cells_new.append(cell)
                continue
            if cell['source'].find('#cuttle-environment') == -1:
                cells_new.append(cell)
                continue
            if cell['source'].find('#cuttle-environment') > -1:
                if cell['source'].find('#cuttle-environment-' + env_name + '-disable') > -1:
                    continue
                if cell['source'].find('#cuttle-environment-' + env_name + '\n') > -1:
                    cells_new.append(cell)
                    continue

        notebook.cells = cells_new

        return notebook
