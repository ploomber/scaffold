"""
Commands to run common tasks such as installing dependencies such as
setup virtual environment, run tests, generate distribution files, etc.

Requires invoke (pip install invoke). For help run "inv -h", to list
commands "inv -l"

Source code for simple commands can be included here, for large ones, save it
in the bin/ folder
"""
from invoke import task
from lib import conda


@task
def setup(c):
    """Setup development environment
    """
    print('Creating conda environment...')
    c.run('conda env create environment.yml --force')
    print('Installing package...')
    conda.run_in_env(c, 'pip install --editable .[dev]', env='package_name')


@task(
    help={
        'inplace':
        'Runs tests in the current environment '
        '(calling pytest directly), otherwise uses nox.'
    })
def test(c, inplace=False):
    """Run tests
    """
    if inplace:
        print('Runnin tests in the current environment...')
        c.run('pytest tests/', pty=True)
    else:
        c.run('nox', pty=True)


@task
def release(c):
    """Create a new version of this project
    """
    pass


@task
def export(c):
    """Export project to Airflow or Kubernetes from a given version
    """
    # TODO: how do we renconcile adding a new version, generating a zip
    # distribution file and exporting to airflow/kubernetes?
    # release should mark the project at a given time, export can move to that
    # point and generate the necessary files to run in airflow/kubernetes
    pass
