"""
API for creating scaffolding projects
"""
import itertools
import os
import shutil
import re
from pathlib import Path
import click

try:
    from importlib import resources
except ImportError:
    # python < 3.7
    import importlib_resources as resources

import ploomber_scaffold


def copy_template(path, package, conda):
    """Copy template files to path
    """
    with resources.path(ploomber_scaffold, 'template') as path_to_template:
        shutil.copytree(path_to_template, path)

    if not package:
        simplify(path)

    # TODO: remove pytest if not a package

    if conda:
        (path / 'requirements.txt').unlink()
        (path / 'requirements.dev.txt').unlink()
    else:
        (path / 'environment.yml').unlink()
        (path / 'environment.dev.yml').unlink()


def simplify(path):
    to_delete = [
        'MANIFEST.in',
        'setup.cfg',
        'setup.py',
        'tests',
        'versioneer.py',
        Path('src', 'package_name', '_version.py'),
        Path('src', 'package_name', '__init__.py'),
    ]

    for f in to_delete:
        path_to_f = path / f

        if path_to_f.is_file():
            path_to_f.unlink()
        else:
            shutil.rmtree(path_to_f)

    base_path = path / 'src' / 'package_name'

    for f in itertools.chain(base_path.glob('**/*'), base_path.glob('*')):
        f = Path(f)

        if f.is_dir():
            f.mkdir(exist_ok=True, parents=True)
        else:
            target = path / f.relative_to(path / 'src' / 'package_name')
            target.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy(f, target)

    shutil.rmtree(path / 'src')
    Path(path, '.gitattributes').unlink()
    Path(path, 'pipeline.yaml').unlink()

    with resources.path(ploomber_scaffold, 'simple') as path_to_simple:
        shutil.copy(path_to_simple / 'pipeline.yaml', path / 'pipeline.yaml')


def is_valid_package_name(package_name):
    match = re.match(r'^[\w]+$', package_name) or False
    return match and not package_name[0].isnumeric()


def last_part(project_path):
    return project_path.parts[-1]


def request_project_path():
    project_path = Path(input('Enter project name: '))
    pkg_name = last_part(project_path)
    return project_path, pkg_name


def render_template(path, package_name):
    """
    Replace references to "package_name" in the template for the name selected
    by the user
    """
    for dirpath, _, filenames in os.walk(path):
        # replace if file has this extension or is .gitignore
        paths = [
            Path(dirpath, f) for f in filenames if Path(f).suffix in {
                '.py',
                '.md',
                '.yml',
                '.yaml',
                '.sh',
                '.sql',
                '.in',
                '.cfg',
            } or f in {'.gitignore', '.gitattributes'}
        ]

        for p in itertools.chain(paths):
            p = Path(p)
            new = p.read_text().replace('package_name', package_name)
            p.write_text(new)

    pkg_dir = path / 'src' / 'package_name'

    if pkg_dir.exists():
        pkg_dir.rename(path / 'src' / package_name)


def cli(project_path, package=False, conda=False):
    """
    Scaffolds a project

    Parameters
    ----------
    project_path : str
        Project's root folder

    package : bool, default=False
        Whether to create a packaged project (with a setup.py file and
        versioneer) or a simple layout

    conda : bool, default=False
        If True, it adds a conda environment.yml file otherwise
        requirements.txt
    """
    project_path = None if not project_path else Path(project_path)

    click.echo('Enter project name:\n* Alphanumeric\n* Lowercase\n'
               '* May contain underscores\n'
               '* First character cannot be numeric\n')

    if project_path is None:
        project_path, pkg_name = request_project_path()

        # TODO: when package is false, do not check this
        while not is_valid_package_name(pkg_name):
            click.echo(
                f'{pkg_name!r} is not a valid package name, choose another.')
            project_path, pkg_name = request_project_path()
    else:
        pkg_name = last_part(project_path)

        if not is_valid_package_name(pkg_name):
            raise ValueError('"%s" is not a valid package identifier, '
                             'choose another.' % pkg_name)

    if project_path.is_dir() and len(os.listdir(project_path)):
        raise click.ClickException(
            f'{str(project_path)!r} is a non-empty directory')
    elif project_path.is_file():
        raise click.ClickException(
            f'{str(project_path)!r} is an existing file')

    copy_template(project_path, package=package, conda=conda)

    render_template(project_path, pkg_name)

    path_pipeline = project_path / 'src' / pkg_name / 'pipeline.yaml'
    path_setup = project_path / 'setup.py'

    # TODO: print path depending on pacakge or not
    # TODO: change add deps message (they should be in env or reqs file)
    click.secho(f'\nDone. Pipeline declaration: {path_pipeline!s}\n',
                fg='green')
    click.echo('Next steps:\n')
    click.secho(f'1. Add extra dependencies to {path_setup!s}\n'
                f'2. Move to {project_path!s}/ and setup the environment'
                ' with: ploomber install')
