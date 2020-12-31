import click
import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter
import os

def main():    
    body ='''
from flask import Flask
from flask import request
app = Flask(__name__)

'''

    for cell in notebook.cells:
        if cell.cell_type == 'code':
            if 'route' in cell.cuttle_config:
                variable_code = ''

                try:
                    method = cell.cuttle_config.method
                except:
                    method = 'GET'

                func_name = '{method}_'.format(method=method.lower()) + '_'.join(cell.cuttle_config.route.split('/'))

                body = body + '''@app.route('{route}', methods=['{method}'])
def {func_name}():'''.format(route=cell.cuttle_config.route, func_name=func_name, method=method)

                for sourceline in cell.source.split('\n'):
                    body = body + '\n' + '    ' + sourceline

                body = body + '\n' + '    ' + 'return {response}'.format(response=cell.cuttle_config.response) + '\n\n'
            else:
                body = body + cell.source + '\n\n'

    body = body + '''
if __name__ == '__main__':
    app.run()'''

    os.makedirs(output_path, exist_ok=True)

    output_file_path = os.path.join(output_path, 'main.py')

    f = open(output_file_path, "w")
    f.write(body)
    f.close()

@click.command()
def cli():
    main()
    pass
