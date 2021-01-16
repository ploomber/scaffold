import zipfile
import os
import subprocess
from pathlib import Path
import shutil
from itertools import chain

import pytest

from ploomber_scaffold import scaffold


@pytest.mark.parametrize('name, valid', [
    ('project', True),
    ('project123', True),
    ('pro_jec_t', True),
    ('pro-ject', False),
    ('1234', False),
    ('a project', False),
])
def test_is_valid_package_name(name, valid):
    assert scaffold.is_valid_package_name(name) is valid


def test_cli(tmp_directory):
    scaffold.cli(project_path='my_new_project')
    os.chdir('my_new_project')

    # setup command
    assert not subprocess.run(['invoke', 'setup']).returncode

    # test command
    script = """
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    invoke test --inplace
    """
    Path('test.sh').write_text(script)

    assert not subprocess.run(['bash', 'test.sh']).returncode

    # test run pipeline
    script = """
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    ploomber build
    """
    Path('build.sh').write_text(script)

    assert not subprocess.run(['bash', 'build.sh']).returncode

    # test installing project from wheel
    script = """
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    pip uninstall my_new_project --yes
    python setup.py bdist_wheel
    pip install dist/my_new_project-0.1.dev0-py3-none-any.whl
    ploomber build
    """
    Path('build_from_wheel.sh').write_text(script)

    assert not subprocess.run(['bash', 'build_from_wheel.sh']).returncode


def test_scaffold_wheel_contents(tmp_path):
    """Make sure the wheel does not contain stuff it shouldn't have
    """
    if Path('build').exists():
        shutil.rmtree('build')

    if Path('dist').exists():
        shutil.rmtree('dist')

    subprocess.run(['python', 'setup.py', 'bdist_wheel'])
    whl_name = os.listdir('dist')[0]

    with zipfile.ZipFile(Path('dist', whl_name), 'r') as zip_ref:
        zip_ref.extractall(tmp_path)

    path = Path(tmp_path, 'ploomber_scaffold', 'template')

    assert not (path / 'dist').exists()
    assert not (path / 'build').exists()
    assert not (path / '.nox').exists()

    files_and_dirs = chain(
        *[dirnames + filenames for _, dirnames, filenames in os.walk(path)])

    hidden = [
        f for f in files_and_dirs if f.startswith('.')
        if f not in {'.gitkeep', '.gitignore'}
    ]

    assert not hidden

    dirs = ['doc', 'exploratory', 'lib', 'products', 'src', 'tests']
    assert all((path / dir_).exists() for dir_ in dirs)