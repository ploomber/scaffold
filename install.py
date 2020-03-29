import shutil
import re
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Install template')
parser.add_argument('--name', type=str, help='Package name', default=None)
args = parser.parse_args()

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


root = ('template-master', 'template')

files_to_replace = [
    ('setup.py', ),
    ('README.md', ),
    ('environment.yml', ),
    ('tests', 'test_import_pkg.py')
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
