import click
import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter
import os

def main():
    exporter = PythonExporter()

    (body, resources) = exporter.from_notebook_node(notebook)
    
    try:
        os.mkdir('output')
        os.mkdir('output/test-1/')
    except:
        print('output folder already exists')
        pass
    f = open("output/test-1/mnist.py", "w")
    f.write(body)
    f.close()
    

@click.command()
def cli():
    main()
    pass

main()
