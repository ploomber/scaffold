
print("""
Python packages should also have short, all-lowercase names,
although the use of underscores is discouraged."

Source: https://www.python.org/dev/peps/pep-0008/
""")

package_name = input('Package name: ')

# TODO: validate package name

files_to_replace = [
    'setup.py',
    'README.md',
    'environment.yml'
    'tests/test_import_pkg.py'
]
