import json
import os
import nbformat
import logging
from tokenize import tokenize, tok_name
from io import BytesIO

logger = logging.getLogger()

class CuttleEngine:
    def __init__(self, path = 'cuttle.json'):
        self.config_file_name = path

        config_file = open(self.config_file_name, "r")
        config_string = config_file.read()

        self.config = json.loads(config_string)

        config_file.close()

    def setHomePath(self, path):
        self.home_path = path

    def getEnvironments(self):
        return self.config['environments'].keys()

    def transform(self, env_name):
        plugin_path = os.path.join(os.path.dirname(__file__), 'transform', self.config['environments'][env_name]['transformer'], 'main.py')
        notebook_path = os.path.join(self.home_path, self.config['notebook'])
        output_file_path = os.path.join(self.home_path, 'output', env_name)

        logger.info("Plugin path: " + plugin_path)

        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)

        nb = self._envtransform(nb, env_name)

        ns = {
            'notebook': nb,
            'output_path': output_file_path
        }

        with open(plugin_path) as f:
            code = compile(f.read(), plugin_path, 'exec')
            eval(code, ns, ns)

        return ns['cli']

    def deploy(self, env_name):
        platform_path = os.path.join(os.path.dirname(__file__), 'platform', self.config['environments'][env_name]['platform'], 'main.py')
        output_file_path = os.path.join(self.home_path, 'output', env_name)

        ns = {
            'output_path': output_file_path,
            'cuttle_config': self.config['environments'][env_name]
        }

        with open(platform_path) as f:
            code = compile(f.read(), platform_path, 'exec')
            eval(code, ns, ns)

        return ns['cli']

    def _parsecommentcuttlebase(self, comment):
        try:
            cuttle_identifier = comment[0:7]
            environment_indentifier = comment[8:19]
            environment_comment = False
            action = None

            if cuttle_identifier != '#cuttle':
                return None, None

            if environment_indentifier == 'environment':
                environment_comment = True

            if environment_comment:
                action = comment[20:]
            else:
                action = comment[8:]
        except:
            return None, None

        return action, environment_comment

    def _celltransform(self, cell, env_name):
        if cell['cell_type'] != 'code':
            return cell

        cuttle_config_object = {}

        g = tokenize(BytesIO(cell['source'].encode('utf-8')).readline)
        cell_tokens = list(g)

        for g_ in cell_tokens:
            if tok_name[g_.type] == 'COMMENT': # Checks if token is a comment
                action, environment_comment = self._parsecommentcuttlebase(g_.string.split(" ")[0])

                if action == None:
                    continue

                if environment_comment:
                    envs = g_.string.split(" ")[1].split(",")

                    if env_name not in envs:
                        continue

                if action == 'disable':
                    return None

                if action in ['config', 'set-config']:
                    cuttle_config = g_.string.split(" ")[2:]
                    
                    for config in cuttle_config:
                        cuttle_config_object[config.split('=')[0]] = config.split('=')[1]

                if action in ['assign', 'get-config']:
                    if action == 'assign':
                        cuttle_value = g_.string.split(" ")[2]
                    else:
                        cuttle_value = self.config['environments'][env_name][g_.string.split(" ")[2]]
                    
                    line_tokens = list(filter(lambda x: x.line == g_.line, cell_tokens))
                    name = None

                    for line_token in line_tokens:
                        if tok_name[line_token.type] == 'NAME':
                            name = line_token.string
                            break

                    if name == None:
                        logger.error("assign or get-config used with invalid variable assignment")
                        break
                    
                    if action == 'assign':
                        variable_assignment_string = name + " = " + cuttle_value + "\n"
                    else:
                        if isinstance(cuttle_value, str):
                            variable_assignment_string = name + ' = "' + cuttle_value + '"' + "\n"
                        else:
                            variable_assignment_string = name + " = " + str(cuttle_value) + "\n"

                    cell.source = cell.source.replace(g_.line, variable_assignment_string)

        cell['cuttle_config'] = cuttle_config_object

        return cell

    def _envtransform(self, notebook, env_name):
        cells = notebook.cells
        cells_new = []

        for cell in cells:
            cell = self._celltransform(cell, env_name)

            if cell != None:
                cells_new.append(cell)

        notebook.cells = cells_new

        return notebook
