import click
import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter
import os

def main():
    print(notebook)
    
    body ='''
from flask import Flask
from flask import request
app = Flask(__name__)

'''

    for cell in notebook.cells:
        if cell.cell_type == 'code':
            if 'route' in cell.cuttle_config:
                variable_code = ''
                for param in cell.cuttle_config.query_params.split(','):
                    variable_code = variable_code + '''
    {param} = request.args.get('{param}')'''.format(param=param)

                body = body + '''@app.route('{route}')
def hello():'''.format(route=cell.cuttle_config.route)

                body = body + variable_code

                for sourceline in cell.source.split('\n'):
                    body = body + '\n' + '    ' + sourceline

                body = body + '\n' + '    ' + 'return {response}'.format(response=cell.cuttle_config.response) + '\n'

    body = body + '''
if __name__ == '__main__':
    app.run()'''

    f = open("test2.py", "w")
    f.write(body)
    f.close()

@click.command()
def cli():
    main()
    pass
