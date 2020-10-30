import click
import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter
import os

def main():
    exporter = PythonExporter()

    (body, resources) = exporter.from_notebook_node(notebook)

    f = open("test.py", "w")
    f.write(body)
    f.close()

@click.command()
def cli():
    main()
    pass
