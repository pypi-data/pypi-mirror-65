import click
import os
from pathlib import Path
import yaml

import pydproc.scripts.workflow as workflow

@click.group()
def pydproc():
    pass

@click.command()
@click.option('--ymlfile', default='', help='Path to yml file with input parameters')
def build(ymlfile):
    if ymlfile == '' or not Path(ymlfile).exists():
        click.confirm("No valid ymlfile found. Build new specs?", abort=True)
        new_specs = workflow.buildspecs()
        ymlfile = Path(os.getcwd) / 'new_spec.yml'
        with (ymlfile).open('w+') as save_file:
            save_file.write(yaml.dump(new_specs))

    workflow.fromyml(ymlfile)

@click.command()
@click.argument('save_path')
def buildyml(save_path):
    save_path = Path(os.path.abspath(save_path))
    new_specs = workflow.buildspecs()
    with (save_path).open('w+') as save_file:
        save_file.write(yaml.dump(new_specs))


@click.command()
@click.argument('proc_name', nargs=1)
def start(proc_name):
    """ COMMAND: Name of process. """
    workflow.start(proc_name)

@click.command()
@click.argument('run_name', nargs=1)
def stop(run_name):
    """ COMMAND: Name of running container file. """
    workflow.stop(run_name)

@click.command()
@click.argument('run_name', nargs=1)
def remove(run_name):
    """ COMMAND: Name of running container file. """
    workflow.remove(run_name)

@click.command()
@click.argument('run_name', nargs=1)
def restart(run_name):
    """ COMMAND: Name of running container file. """
    workflow.restart(run_name)

@click.command()
@click.argument('run_name', nargs=1)
@click.argument('destination', nargs=1)
def getdata(run_name, destination):
    """ COMMAND: Name of running container file.
        COMMAND: Name of destination. """
    workflow.get_data(run_name, destination)

@click.command()
@click.option('--run_name', default=None, help='Name of running container file.')
def ls(run_name):
    workflow.list_containers(run_name)

@click.command()
@click.argument('path', nargs=1)
def validate(path):
    """ COMMAND: Path to YML file. """
    workflow.validate(path)

# Add all click commands under pydproc group

pydproc.add_command(build)
pydproc.add_command(start)
pydproc.add_command(stop)
pydproc.add_command(remove)
pydproc.add_command(restart)
pydproc.add_command(getdata)
pydproc.add_command(ls)
pydproc.add_command(validate)
pydproc.add_command(buildyml)
