import click

from cli.command_utils import info_message
from disco import Config

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group('config', context_settings=CONTEXT_SETTINGS)
def config_commands():
    """Manage disco local config."""


@config_commands.command('set-cluster-id', help='Set the cluster ID')
@click.argument('value')
def set_cluster_id(value):
    """
    Set a configuration item

    """
    config = Config()
    config.set("cluster_id", value)


@config_commands.command('set-cluster-instance-type', help='Set the cluster instance type (s, m, l, ...)')
@click.argument('value')
def set_cluster_instance_type(value):
    """
    Set a configuration item

    """
    config = Config()
    config.set("cluster_instance_type", value)


@config_commands.command('set-docker-image-id', help='Set the docker image ID to use for jobs')
@click.argument('value')
def docker_image_id(value):
    """
    Set a configuration item

    """
    config = Config()
    config.set("docker_image_id", value)


@config_commands.command('view', help='View configuration')
def view():
    """
    Print configuration to screen

    """
    config = Config()
    for key in config.config:
        info_message(f"{key}: {config.config[key]}")


@config_commands.command('unset', help='Resets a configuration item')
@click.argument('key')
def reset(key):
    """
    Reset a key by deleting it from the file

    """
    config = Config()
    config.reset(key)
