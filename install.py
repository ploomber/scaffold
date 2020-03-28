import re
from pathlib import Path

print("""
Python packages should also have short, all-lowercase names,
although the use of underscores is discouraged."

Source: https://www.python.org/dev/peps/pep-0008/
""")

package_name = input('Package name: ')

root = ('template-master', 'template')

# TODO: validate package name
re.match(r'')

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
    process_path(path)

# rename file src/package_name

# move contents from template/ to the current working directory

# delete extra files

# rename root folder
