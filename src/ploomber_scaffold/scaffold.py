"""
API for creating scaffolding projects
"""
import os
import sys
import shutil
import re
from pathlib import Path
import argparse
from importlib import resources
import ploomber_scaffold


def copy_template(path):
    """Copy template files to path
    """
    with resources.path(ploomber_scaffold, 'template') as path_to_template:
        shutil.copytree(path_to_template, path)


def is_valid_package_name(package_name):
    return (re.match(r'^[\w]+$', package_name)
            and not package_name[0].isnumeric())


def render_template(name):
    """
    Replace references to "package_name" in the template for the name selected
    by the user
    """
    pass


def cli():
    parser = argparse.ArgumentParser(description='Create scaffold')
    parser.add_argument('--path', type=Path, help='Path', default=None)
    args = parser.parse_args()
    target = args.path

    print("""
Python packages should also have short, all-lowercase names,
although the use of underscores is discouraged."

Source: https://www.python.org/dev/peps/pep-0008/

""")

    if target is None:
        pkg_name = input('Package name: ')

        while not is_valid_package_name(pkg_name):
            print('"%s" is not a valid package identifier, choose another.' %
                  pkg_name)
            pkg_name = input('Package name: ')
    else:
        pkg_name = args.path.parts[-1]

        if not is_valid_package_name(pkg_name):
            raise ValueError('"%s" is not a valid package identifier, '
                             'choose another.' % pkg_name)

    if target.is_dir() and len(os.listdir(target)):
        raise ValueError(f'{target!r} is a non-empty directory')
    elif target.is_file():
        raise ValueError(f'{target!r} is an existing file')

    print(f'Copying template to {str(target)!r}')
    copy_template(target)
    print('Done.')


if __name__ == '__main__':
    cli()
