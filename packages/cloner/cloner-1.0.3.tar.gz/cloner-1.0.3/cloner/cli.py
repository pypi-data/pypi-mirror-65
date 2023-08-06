import click
import os
import subprocess

from cloner.arg_parser import ArgParser


class ClonerException(click.ClickException):
    exit_code = 1


@click.command()
@click.argument('args', nargs=-1)
def cli(args):
    cloner_path = os.getenv('CLONER_PATH')
    if cloner_path is None:
        msg = 'CLONER_PATH environment variable must be defined'
        raise ClonerException(msg)
    cloner_path = os.path.expanduser(cloner_path)
    ap = ArgParser(args)
    local_path = os.path.join(cloner_path, ap.local_path_tail)
    subprocess.call(["git", "clone", ap.url, local_path])
