import shutil
from invoke import task
from lib import conda, versioneer


@task
def setup(c, editable=True, version='3.9', inline=False):
    """Setup development environment
    """
    if inline:
        print('Installing in current environment...')
    else:
        print('Creating conda environment...')
        c.run(f'conda create --name scaffold python={version} --force --yes')

    print('Installing package...')
    flag = '--editable' if editable else ''
    pip_cmd = f'pip install {flag} .[dev]'

    if inline:
        c.run(pip_cmd)
    else:
        conda.run_in_env(c, pip_cmd, env='scaffold')

    if not shutil.which('git'):
        print(
            '[WARNING] git is required to run tests but it is not installed...'
        )


@task(
    help={
        'inline':
        'Runs tests in the current environment '
        '(calling pytest directly), otherwise uses nox.'
    })
def test(c, inline=False, pty=True):
    """Run tests
    """
    if inline:
        print('Running tests in the current environment...')
        c.run('pytest tests/', pty=pty)
    else:
        c.run('nox', pty=pty)


@task
def release(c):
    """Create a new version of this project
    """
    versioneer.version(project_root='.', tag=True)


@task
def upload(c, tag, production=True):
    """Upload to PyPI (prod by default): inv upload {tag}
    """
    versioneer.upload(tag, production=production)
