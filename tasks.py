from invoke import task
from lib import conda, versioneer


@task
def setup(c):
    """Setup development environment
    """
    print('Creating conda environment...')
    c.run('conda create --name scaffold python=3.8 --force --yes')
    print('Installing package...')
    conda.run_in_env(c, 'pip install --editable .[dev]', env='scaffold')


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
    versioneer.release(project_root='.', tag=True)


@task
def upload(c, tag, production=False):
    versioneer.upload(tag, production=production)
