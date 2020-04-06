"""
Installation script
"""
import shutil
import re
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Install template in the '
                                 'current directory')
parser.add_argument('--name', type=str, help='Package name', default=None)
parser.add_argument('--path', type=str,
                    help='Path to template (folder where setup.py is)',
                    default='template-master/template/')
args = parser.parse_args()

if args.path is None:
    root = ('template-master', 'template')
else:
    root = Path(args.path).parts


path_to_setup = Path(*root, 'setup.py')

if not path_to_setup.exists():
    raise FileNotFoundError('Could not find a setup.py file located in '
                            '%s, verify location' % str(path_to_setup))

print("""
Python packages should also have short, all-lowercase names,
although the use of underscores is discouraged."

Source: https://www.python.org/dev/peps/pep-0008/

""")


def is_valid_name(package_name):
    return (re.match(r'^[\w]+$', package_name)
            and not package_name[0].isnumeric())


if args.name is None:
    package_name = input('Package name: ')

    while not is_valid_name(package_name):
        print('"%s" is not a valid package identifier, choose another.'
              % package_name)
        package_name = input('Package name: ')
else:
    package_name = args.name

    if not is_valid_name(package_name):
        raise ValueError('"%s" is not a valid package identifier, '
                         'choose another.' % package_name)

files_to_replace = [
    ('setup.py', ),
    ('README.md', ),
    ('environment.yml', ),
    ('tests', 'test_import_pkg.py'),
    ('distribute', 'main', 'Procfile'),
    ('distribute', 'main', 'build.sh')
]


def process_path(path):
    text_new = path.read_text().replace('package_name', package_name)
    path.write_text(text_new)


for file in files_to_replace:
    path = Path(*(root + file))
    print('Adding "%s" in file %s' % (package_name, path))
    process_path(path)

# rename file src/package_name
target = Path(*root, 'src', package_name)
Path(*root, 'src', 'package_name').rename(target)

# move contents from template/ to the current working directory
for file in Path(*root).glob('*'):
    target = str(file.name)
    print('Moving %s to %s' % (file, target))
    shutil.move(str(file), target)

# delete original folder
print('Removing %s' % root[0])
shutil.rmtree(root[0])

# rename current folder
print('Renaming project root folder to "%s"' % package_name)
