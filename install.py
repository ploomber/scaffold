import os
import shutil
import re
from pathlib import Path

print("""
Python packages should also have short, all-lowercase names,
although the use of underscores is discouraged."

Source: https://www.python.org/dev/peps/pep-0008/
""")

package_name = input('Package name: ')

while not re.match(r'^[\w]+$', package_name) or package_name[0].isnumeric():
    print('"%s" is not a valid package identifier, choose another.'
          % package_name)
    package_name = input('Package name: ')

root = ('template-master', 'template')
root = ('template', )

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

# delete extra files
shutil.rmtree(str(Path(*root)))

# rename current folder
print('Renaming project root folder to "%s"' % package_name)
Path(root[0]).rename(package_name)


# delete files that are part of the root folder
to_remove = ['LICENSE', 'test.sh', 'install.py', 'template/']

for path in to_remove:
    print('Removing %s' % path)
    if path.endswith('/'):
        shutil.rmtree(path)
    else:
        os.remove(path)

print('Done. Check out README.md for next steps.')
