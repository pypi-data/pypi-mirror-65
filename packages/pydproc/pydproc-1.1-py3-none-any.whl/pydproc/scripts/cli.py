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
    """
    Build new process.
    """
    if ymlfile == '' or not Path(ymlfile).exists():
        click.confirm("No valid ymlfile found. Build new specs?", abort=True)
        new_specs = workflow.buildspecs()
        ymlfile = Path(os.getcwd) / 'new_spec.yml'
        with (ymlfile).open('w+') as save_file:
            save_file.write(yaml.dump(new_specs))

    workflow.fromyml(ymlfile)

@click.command()
@click.argument('save_path', nargs=1)
def buildyml(save_path):
    """
    Build new specs for a process and save it to a yml file
    """
    save_path = Path(os.path.abspath(save_path))
    new_specs = workflow.buildspecs()
    with (save_path).open('w+') as save_file:
        save_file.write(yaml.dump(new_specs))


@click.command()
@click.argument('proc_name', nargs=1)
def start(proc_name):
    """ Start new run. """
    workflow.start(proc_name)

@click.command()
@click.argument('run_name', nargs=1)
def stop(run_name):
    """ Indefinitely pause run. """
    workflow.stop(run_name)

@click.command()
@click.argument('run_name', nargs=1)
def remove(run_name):
    """ Remove run. """
    workflow.remove(run_name)

@click.command()
@click.argument('run_name', nargs=1)
def restart(run_name):
    """ Restart stopped run. """
    workflow.restart(run_name)

@click.command()
@click.argument('run_name', nargs=1)
@click.argument('destination', nargs=1)
def getdata(run_name, destination):
    """ Get data from specific run """
    workflow.get_data(run_name, destination)

@click.command()
@click.option('--run_name', default=None, help='Name of running container file.')
def ls(run_name):
    """ List all current runs """
    workflow.list_containers(run_name)

@click.command()
@click.argument('path', nargs=1)
def validate(path):
    """ Validate yml file can be built and run correctly """
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
