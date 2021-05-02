import click
import paramiko
from scp import SCPClient
import nbformat
from nbconvert import PythonExporter
import os

def main():
    dependency_map = {}
    body ='''
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
}

dag = DAG(
    dag_id='branch_without_trigger',
    schedule_interval=None,
    start_date=days_ago(2)
)
'''

    for cell in notebook.cells:
        if cell.cell_type == 'code' and 'task-id' in cell.cuttle_config:
            dependencies = []
            if 'dependency' in cell.cuttle_config:
                dependencies = cell.cuttle_config['dependency'].split(",")

            dependency_map[cell.cuttle_config['task-id']] = dependencies

            body = body + '''\n\ndef {taskid}():'''.format(taskid=cell.cuttle_config['task-id']) 

            for sourceline in cell.source.split('\n'):
                body = body + '\n' + '    ' + sourceline

        elif cell.cell_type == 'code':
            for sourceline in cell.source.split('\n'):
                body = body + '\n' + sourceline

    body = body + '\n'
    for key in dependency_map.keys():
        body = body + '''\n{taskid} = PythonOperator(task_id='{taskid}', python_callable={taskid}, dag=dag)'''.format(taskid=key)

    body = body + '\n'
    for key in dependency_map.keys():
        if len(dependency_map[key]) > 0:
            body = body + '''\n{dependency} >> {taskid}'''.format(taskid=key, dependency="[" + ", ".join(dependency_map[key]) + "]")

    os.makedirs(output_path, exist_ok=True)

    output_file_path = os.path.join(output_path, 'main.py')

    f = open(output_file_path, "w")
    f.write(body)
    f.close()

@click.command()
def cli():
    main()
    pass
