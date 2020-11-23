import json
import os
import nbformat
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO

class CuttleEngine:
    def __init__(self):
        # self.config_file_name = '../prodo.json'
        self.config_file_name = 'cuttle.json'

        config_file = open(self.config_file_name, "r")
        config_string = config_file.read()

        self.config = json.loads(config_string)

    def setHomePath(self, path):
        self.home_path = path

    def getEnvironments(self):
        return self.config['environments'].keys()

    def transform(self, env_name):
        plugin_path = os.path.join(self.home_path, 'transform', self.config['environments'][env_name]['transformer'], 'main.py')
        notebook_path = os.path.join(self.home_path, self.config['notebook'])

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

            cuttle_environments = []
            cuttle_environments_disable = []
            cuttle_comment_config = ''
            cuttle_environment_tag_present = False
            cuttle_environment_disable_tag_present = False
            cuttle_config_object = {}

            g = tokenize(BytesIO(cell['source'].encode('utf-8')).readline)

            for g_ in g:
                if g_.type == 57: # Checks if line is a comment
                    if g_.string.split(" ")[0] == '#cuttle-environment':
                        cuttle_environment_tag_present = True
                        cuttle_environments = g_.string.split(" ")[1:]

                    if g_.string.split(" ")[0] == '#cuttle-environment-disable':
                        cuttle_environment_disable_tag_present = True
                        cuttle_environments_disable = g_.string.split(" ")[1:]

                    if g_.string.split(" ")[0] == '#cuttle-environment-config':
                        if g_.string.split(" ")[1] == env_name:
                            cuttle_config = g_.string.split(" ")[2:]
                            
                            for config in cuttle_config:
                                cuttle_config_object[config.split('=')[0]] = config.split('=')[1]

                    if g_.string.split(" ")[0] == '#cuttle-config':
                        cuttle_config = g_.string.split(" ")[1:]
                            
                        for config in cuttle_config:
                            cuttle_config_object[config.split('=')[0]] = config.split('=')[1]

            cell['cuttle_config'] = cuttle_config_object

            if cuttle_environment_tag_present == True:
                if env_name in cuttle_environments:
                    cells_new.append(cell)
                    continue
            elif cuttle_environment_disable_tag_present == True:
                if env_name not in cuttle_environments_disable:
                    cells_new.append(cell)
                    continue
            else:
                cells_new.append(cell)
                continue

        notebook.cells = cells_new

        return notebook
