"""
API for creating scaffolding projects
"""
import itertools
import os
import shutil
import re
from pathlib import Path

try:
    from importlib import resources
except ImportError:
    # python < 3.7
    import importlib_resources as resources

import ploomber_scaffold
from ploomber_scaffold.exceptions import ScaffoldError

import click
from jinja2 import Template


def _resources_path(dir_name):
    # resources.files added on python 3.9
    # https://www.mail-archive.com/python-bugs-list@python.org/msg451088.html
    if hasattr(resources, 'files'):
        with resources.files(ploomber_scaffold) as p:
            out = p / dir_name
    else:
        with resources.path(ploomber_scaffold, dir_name) as p:
            out = p

    return out


def copy_template(path, package, conda):
    """Copy template files to path
    """
    path_to_template = _resources_path('template')

    shutil.copytree(path_to_template, path)

    path_to_readme = (path / 'README.md')
    readme = Template(path_to_readme.read_text()).render(package=package,
                                                         conda=conda)
    path_to_readme.write_text(readme)

    if not package:
        simplify(path)

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

    path_to_simple = _resources_path('simple')
    shutil.copy(path_to_simple / 'pipeline.yaml', path / 'pipeline.yaml')


def is_valid_package_name(package_name):
    match = re.match(r'^[\w]+$', package_name) or False
    return match and not package_name[0].isnumeric()


def is_valid_project_name(project_name):
    match = re.match(r'^[\w-]+$', project_name)
    return True if match else False


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


def _echo_instructions(package, with_prompt=False):
    text = _get_instructions(package)

    if with_prompt:
        text + '\nEnter project name:'

    click.echo(text)


def _get_instructions(package):
    if package:
        return ('\n\n* Alphanumeric (lowercase), underscore (_) allowed\n'
                '* First character cannot be numeric\n')
    else:
        return ('\n\n* Alphanumeric (lowercase), underscore '
                '(_), hyphen (-) allowed\n'
                '* First character cannot be numeric\n')


def _get_error_message(package, pkg_name):
    return (f'{pkg_name!r} is not a valid name, '
            f'choose another. {_get_instructions(package)}')


def cli(project_path, package=False, conda=None, empty=False):
    """
    Scaffolds a project

    Parameters
    ----------
    project_path : str
        Project's root folder

    package : bool, default=False
        Whether to create a packaged project (with a setup.py file and
        versioneer) or a simple layout

    conda : bool, default=None
        If True, it adds a conda environment.yml file otherwise
        requirements.txt. If None, it uses environment.yml if conda is
        installed

    empty : bool, default=False
        If True, it doesn't add sample tasks
    """
    project_path = None if not project_path else Path(project_path)
    check_name = is_valid_package_name if package else is_valid_project_name
    print_conda_detected = conda is None

    if conda is None:
        conda = True if shutil.which('conda') else False

    if project_path is None:
        _echo_instructions(package=package, with_prompt=True)

        project_path, pkg_name = request_project_path()

        while not check_name(pkg_name):
            click.echo(_get_error_message(package, pkg_name))
            project_path, pkg_name = request_project_path()
    else:
        pkg_name = last_part(project_path)

        if not check_name(pkg_name):
            raise ScaffoldError(_get_error_message(package, pkg_name))

    if project_path.is_dir() and len(os.listdir(project_path)):
        raise ScaffoldError(f'{str(project_path)!r} is a non-empty directory')
    elif project_path.is_file():
        raise ScaffoldError(f'{str(project_path)!r} is an existing file')

    copy_template(project_path, package=package, conda=conda)

    render_template(project_path, pkg_name)

    if package:
        path_pipeline = project_path / 'src' / pkg_name / 'pipeline.yaml'
    else:
        path_pipeline = project_path / 'pipeline.yaml'

    if conda:
        path_deps = project_path / 'environment.yml'
    else:
        path_deps = project_path / 'requirements.txt'

    if print_conda_detected and conda:
        click.echo(f'conda detected, generating {str(path_deps)}')

    if empty:
        if package:
            pkg_root = project_path / 'src' / pkg_name
            shutil.rmtree(pkg_root / 'tasks')
            shutil.rmtree(pkg_root / 'scripts')

            path_to_empty = _resources_path('empty')
            shutil.copy(path_to_empty / 'package.yaml', path_pipeline)

        else:
            shutil.rmtree(project_path / 'tasks')
            shutil.rmtree(project_path / 'scripts')

            path_to_empty = _resources_path('empty')
            shutil.copy(path_to_empty / 'no-package.yaml', path_pipeline)

    click.secho(f'\nPipeline at: {path_pipeline!s}\n')
    click.echo('Next steps:\n')
    click.secho(
        f'Add dependencies to {path_deps!s}\n\n'
        f'$ cd {project_path!s}\n\n'
        '$ ploomber install\n',
        fg='green')
