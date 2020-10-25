import click
import json
import os

from cuttleengine import CuttleEngine

plugin_folder = 'plugin'
config_file_name = 'cuttle.json'
default_notebook_name = 'main.ipynb'
default_plugin_file = 'main.py'

from functools import update_wrapper

def pass_config(f):
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        try:
            config_file = open(config_file_name, "r")
            config_string = config_file.read()
            config = json.loads(config_string)
            kwargs['config'] = config
            return ctx.invoke(f, *args, **kwargs)
        except Exception as e:
            click.echo('Cuttle project not initialized.')
            return
        
    return update_wrapper(wrapper, f)

def load_config(f):
    def wrapper(**kwargs):
        try:
            config_file = open(config_file_name, "r")
            config_string = config_file.read()
            config = json.loads(config_string)
            kwargs['config'] = config
            f(**kwargs)
        except:
            click.echo('Cuttle project not initialized.')
            return

    return wrapper

class Services(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            rv.append(filename)

        rv.sort()
        return rv

    def get_command(self, ctx, name):
        ns = {}
        fn = os.path.join(plugin_folder, name, default_plugin_file)
        with open(fn) as f:
            code = compile(f.read(), fn, 'exec')
            eval(code, ns, ns)
        return ns['cli']

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', help='Unique name for Cuttle environment.', prompt=True, type=str)
@click.option('--transformer', help='Transformer to use along with Cuttle environment.', prompt=True, type=str, default='notebook')
@pass_config
def create(name, transformer, config):
    config['environments'][name] = {
        'transformer': transformer
    }

    config_file = open(config_file_name, "w+")
    json.dump(config, config_file, indent = 4, sort_keys=True)

@cli.command(cls=Services)
@click.pass_context
def transform(ctx):
    try:
        config_file = open(config_file_name, "r")
        config_string = config_file.read()
        config = json.loads(config_string)
        config['home_path'] = os.getcwd()
        ctx.obj = config
    except Exception as e:
        click.echo('Cuttle project not initialized correctly.')
        click.echo(e)
        return

@cli.command()
@click.option('--notebook', help='Notebook file name.', prompt=True, type=str, default=default_notebook_name)
def init(notebook):
    try:
        config_file = open(config_file_name, "r")
        config_string = config_file.read()
        config = json.loads(config_string)
    except Exception as e:
        config = {
            'environments': {}
        }

    config['notebook'] = notebook

    config_file = open(config_file_name, "w+")
    json.dump(config, config_file, indent = 4, sort_keys=True)

if __name__ == "__main__":
    cli()
