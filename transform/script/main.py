import click
import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter
import os

@click.command()
def cli():
    exporter = PythonExporter()

    (body, resources) = exporter.from_notebook_node(notebook)

    os.makedirs(output_path, exist_ok=True)

    output_file_path = os.path.join(output_path, 'main.py')

    f = open(output_file_path, "w")
    f.write(body)
    f.close()
