from functools import update_wrapper
import click
import json
import logging

import os
import sys
import pkg_resources

logger = logging.getLogger()

engine_path = os.path.dirname(os.path.realpath(__file__))
version = pkg_resources.get_distribution("cuttle").version

sys.path.append(engine_path)

from cuttleengine import CuttleEngine

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
@click.option('--log', default=False, is_flag=True)
def cli(log):
    if log==True:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    logger.info("Cuttle CLI version: " + version)
    logger.info("Appending to sys.path: " + os.path.dirname(os.path.realpath(__file__)))
    logger.info("Current working directory: " + os.getcwd())

    pass


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
