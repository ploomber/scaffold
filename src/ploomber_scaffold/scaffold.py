"""
API for creating scaffolding projects
"""
import itertools
import os
import shutil
import re
from pathlib import Path
import argparse

try:
    from importlib import resources
except ImportError:
    # python < 3.7
    import importlib_resources as resources

import ploomber_scaffold


def copy_template(path):
    """Copy template files to path
    """
    with resources.path(ploomber_scaffold, 'template') as path_to_template:
        shutil.copytree(path_to_template, path)


def is_valid_package_name(package_name):
    match = re.match(r'^[\w]+$', package_name) or False
    return match and not package_name[0].isnumeric()


def last_part(project_path):
    return project_path.parts[-1]


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
    pkg_dir.rename(path / 'src' / package_name)


def cli(project_path):
    project_path = None if not project_path else Path(project_path)

    print('Project names should be alphanumeric, all-lowercase.\n'
          'The first character cannot be numeric.\n')

    if project_path is None:
        project_path = Path(input('Project name: '))
        pkg_name = last_part(project_path)

        while not is_valid_package_name(pkg_name):
            print(f'{pkg_name!r} is not a valid name, choose another.')
            pkg_name = input('Project name: ')
    else:
        pkg_name = last_part(project_path)

        if not is_valid_package_name(pkg_name):
            raise ValueError('"%s" is not a valid package identifier, '
                             'choose another.' % pkg_name)

    if project_path.is_dir() and len(os.listdir(project_path)):
        raise ValueError(f'{str(project_path)!r} is a non-empty directory')
    elif project_path.is_file():
        raise ValueError(f'{str(project_path)!r} is an existing file')

    copy_template(project_path)
    render_template(project_path, pkg_name)
    readme_path = project_path / 'README.md'
    print(f'Done. Check out {readme_path!s} to get started.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create scaffold')
    parser.add_argument('--path', type=str, help='Path', default=None)
    args = parser.parse_args()
    cli(project_path=args.path)
