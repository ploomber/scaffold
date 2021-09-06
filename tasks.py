import shutil
from invoke import task
from lib import conda, versioneer


@task
def setup(c, editable=True, version='3.9'):
    """Setup development environment
    """
    print('Creating conda environment...')
    c.run(f'conda create --name scaffold python={version} --force --yes')
    print('Installing package...')
    flag = '--editable' if editable else ''
    conda.run_in_env(c, f'pip install {flag} .[dev]', env='scaffold')

    if not shutil.which('git'):
        print(
            '[WARNING] git is required to run tests but it is not installed...'
        )


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
        print('Running tests in the current environment...')
        c.run('pytest tests/', pty=True)
    else:
        c.run('nox', pty=True)


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
