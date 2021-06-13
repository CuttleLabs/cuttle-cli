from functools import update_wrapper
import click
import json
from shutil import copyfile
import shutil
import scp

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from .cuttleengine import CuttleEngine

config_file_name = 'cuttle.json'
default_notebook_name = 'main.ipynb'
default_plugin_file = 'main.py'


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
            print(e)
            click.echo('Cuttle project not initialized.')
            return

    return update_wrapper(wrapper, f)


class Transformers(click.MultiCommand):
    def list_commands(self, ctx):
        cuttleengine = CuttleEngine()
        cuttleengine.setHomePath(os.getcwd())
        ctx.obj = cuttleengine

        return ctx.obj.getEnvironments()

    def get_command(self, ctx, name):
        cuttleengine = CuttleEngine()
        cuttleengine.setHomePath(os.getcwd())

        return cuttleengine.transform(name)


class Platforms(click.MultiCommand):
    def list_commands(self, ctx):
        cuttleengine = CuttleEngine()
        cuttleengine.setHomePath(os.getcwd())
        ctx.obj = cuttleengine

        return ctx.obj.getEnvironments()

    def get_command(self, ctx, name):
        cuttleengine = CuttleEngine()
        cuttleengine.setHomePath(os.getcwd())

        return cuttleengine.deploy(name)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--env_name', help='The name of deployment environment', prompt=True, type=str)
@pass_config
def deploy(env_name, config):
    try:
        dep = config['environments'][env_name]
        plugin_path = os.path.join(
            'platform', config['environments'][env_name]['platform'], 'main.py')
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
@click.option('--transformer', help='Transformer to use along with Cuttle environment.', prompt=True, type=str)
@pass_config
def create(env_name, platform, transformer, config):
    config_file_path = os.path.join(os.getcwd(), config_file_name)

    config['environments'][env_name] = {
        'platform': platform,
        'transformer': transformer
    }

    config_file = open(config_file_path, "w+")
    json.dump(config, config_file, indent=4, sort_keys=True)


@cli.command(cls=Transformers)
def transform():
    pass


@cli.command(cls=Platforms)
def deploy():
    pass


@cli.command()
@click.option('--notebook', help='Notebook file name.', prompt=True, type=str, default=default_notebook_name)
def init(notebook):
    config_file_path = os.path.join(os.getcwd(), config_file_name)
    try:
        config_file = open(config_file_path, "r")
        config_string = config_file.read()
        config = json.loads(config_string)
    except Exception as e:
        config = {
            'environments': {}
        }

    config['notebook'] = notebook

    config_file = open(config_file_path, "w+")
    json.dump(config, config_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    cli()
