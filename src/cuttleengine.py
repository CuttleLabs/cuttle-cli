import json
import os
import nbformat
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO

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

        nb = self.envtransform(self.config, nb, env_name)

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

            cuttle_comment_config = ''

            g = tokenize(BytesIO(cell['source'].encode('utf-8')).readline)

            for g_ in g:
                if g_.type == 57:
                    cuttle_comment_config = g_.string

            if cuttle_comment_config.find('#cuttle-environment') == -1:
                cells_new.append(cell)
                continue

            if cuttle_comment_config == '#cuttle-environment-' + env_name + '-disable':
                continue

            if cuttle_comment_config == '#cuttle-environment-' + env_name:
                cells_new.append(cell)
                continue

        notebook.cells = cells_new

        return notebook
