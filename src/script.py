import click
import json
import os
from shutil import copyfile
import shutil
import scp
import sys

from cuttleengine import CuttleEngine

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

class Services(click.MultiCommand):
    def list_commands(self, ctx):
        cuttleengine = CuttleEngine()
        cuttleengine.setHomePath(os.getcwd())
        ctx.obj = cuttleengine

        return ctx.obj.getEnvironments()

    def get_command(self, ctx, name):
        cuttleengine = CuttleEngine()
        cuttleengine.setHomePath(os.getcwd())

        return cuttleengine.transform(name)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--env_name', help='The name of deployment environment', prompt=True, type=str)
@pass_config
def deploy(env_name, config):
    try:
        dep = config['environments'][env_name]
        plugin_path = os.path.join('platform', config['environments'][env_name]['platform'],'main.py')
        with open(plugin_path) as f:
            ns = {
                'config': dep
            }
            code = compile(f.read(), plugin_path, 'exec')
            eval(code, ns, ns)
    except Exception as e:
        print(e)


@cli.command()
@click.option('--env_name', help='Unique name for Cuttle environment.', prompt=True, type=str)
@click.option('--platform', help='The platform you want to deploy on', prompt=True, type=str)
@click.option('--transformer', help='Transformer to use along with Cuttle environment.', prompt=True, type=str, default='notebook')
@click.option('--username', help='Username to login', prompt=True)
@click.option('--pem_file', help='Name of the pem file', prompt=True)
@click.option('--ip', help='Enter the public IP to ssh into it', prompt=True)
@pass_config
def create(env_name, platform, transformer, username, pem_file, ip, config):
    config['environments'][env_name] = {
        'platform': platform,
        'transformer': transformer,
        'username': username,
        'pem_file': pem_file,
        'ip': ip
    }

    config_file = open(config_file_name, "w+")
    json.dump(config, config_file, indent = 4, sort_keys=True)

# @cli.command(cls=Services)
# @click.pass_context
# @pass_config
# def transform(ctx, config):
#     pass

@cli.command()
@click.option('--env_name', help='Enter env name', prompt=True, type=str)
@pass_config
def transform(env_name, config):
    try:
        cuttleengine = CuttleEngine()
        cuttleengine.setHomePath(os.getcwd())
        cuttleengine.transform(env_name)
    except Exception as e:
        print('exception occurred: ')
        print(e)


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
