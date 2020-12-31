"""
Commands to run common tasks such as installing dependencies such as
setup virtual environment, run tests, generate distribution files, etc.

Requires invoke (pip install invoke). For help run "inv -h", to list
commands "inv -l"

Source code for simple commands can be included here, for large ones, save it
in the bin/ folder
"""
from invoke import task


@task
def setup(c):
    """Setup virtual environment
    """
    pass


@task
def lock(c):
    """Pin virtual environment
    """
    pass


@task
def test(c):
    """Run tests
    """
    # generate lock file
    pass


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