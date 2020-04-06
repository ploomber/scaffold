"""
Installation script
"""
import sys
import shutil
import re
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Install template in the '
                                 'current directory')
parser.add_argument('--name', type=str, help='Package name', default=None)
args = parser.parse_args()

path_to_root = Path(sys.argv[0]).resolve().parent
# infer setup.py location
setup_py_parent = (path_to_root / 'template').parts
path_to_setup = Path(*setup_py_parent, 'setup.py')

if not path_to_setup.exists():
    raise FileNotFoundError('Could not find a setup.py file located in '
                            '%s, verify location' % str(path_to_setup))


# delete all extra files
for file in path_to_root.glob('*'):
    if file.name not in ('template', 'install.py'):
        print('Deleting %s' % file)
        if file.is_file():
            file.unlink()
        else:
            shutil.rmtree(str(file))

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
    path = Path(*(setup_py_parent + file))
    print('Adding "%s" in file %s' % (package_name, path))
    process_path(path)

# rename file src/package_name
target = Path(*setup_py_parent, 'src', package_name)
Path(*setup_py_parent, 'src', 'package_name').rename(target)

# move contents from template/ to the current working directory
for file in Path(*setup_py_parent).glob('*'):
    target = str(file.name)
    print('Moving %s to %s' % (file, target))
    shutil.move(str(file), target)


print('Deleting %s' % path_to_root)
shutil.rmtree(str(path_to_root))
