# files where we have to replace package_name
files_to_replace = [('setup.py', ), ('setup.sh', ), ('README.md', ),
                    ('environment.yml', ), ('tests', 'test_import_pkg.py'),
                    ('distribute', 'main', 'Procfile'),
                    ('distribute', 'main', 'build.sh')]


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

if running_in_parent:
    print('Deleting %s' % path_to_root)
    shutil.rmtree(str(path_to_root))
else:
    path_to_template = path_to_root / 'template'
    print('Deleting %s' % path_to_template)
    shutil.rmtree(str(path_to_template))

    path_to_install_py = path_to_root / 'install.py'
    print('Deleting %s' % path_to_install_py)
    path_to_install_py.unlink()
