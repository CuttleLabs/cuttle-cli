import click
import json
import os

plugin_folder = os.path.join(os.path.dirname(__file__), 'service')

class Services(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            rv.append(filename)

        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name, 'main.py')
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']

@click.group()
def cli():
    pass

@cli.command(cls=Services)
@click.pass_context
def deploy(ctx):
    try:
        config_file = open("prodo.json", "r")
        config_string = config_file.read()
        config = json.loads(config_string)
        config['home_path'] = os.getcwd()
        ctx.obj = config
    except Exception as e:
        print(e)
        click.echo('Prodo project not initialized correctly.')
        return

@cli.command()
def init():
    try:
        config_file = open("prodo.json", "r")
        config_string = config_file.read()
        config = json.loads(config_string)
    except Exception as e:
        config = {
            'services': {}
        }

    if 'notebook' in config.keys():
        notebook_default = config['notebook']
    else:
        notebook_default = 'main.ipynb'

    notebook_file = input("Notebook file name (default - %s): " % notebook_default)

    if notebook_file == "":
        config['notebook'] = notebook_default
    else:
        config['notebook'] = notebook_file

    config_file = open("prodo.json", "w+")
    json.dump(config, config_file, indent = 4, sort_keys=True)
