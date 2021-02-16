import os
import subprocess
from pathlib import Path
import shutil
from itertools import chain
import zipfile


def test_scaffold_wheel_contents(tmp_path):
    """Make sure the wheel does not contain stuff it shouldn't have
    """
    if Path('build').exists():
        shutil.rmtree('build')

    if Path('dist').exists():
        shutil.rmtree('dist')

    subprocess.run(['python', 'setup.py', 'bdist_wheel'], check=True)
    whl_name = os.listdir('dist')[0]

    with zipfile.ZipFile(Path('dist', whl_name), 'r') as zip_ref:
        zip_ref.extractall(tmp_path)

    path = Path(tmp_path, 'ploomber_scaffold', 'template')

    assert not (path / 'dist').exists()
    assert not (path / 'build').exists()
    assert not (path / '.nox').exists()
    assert not (path / '__pycache__').exists()

    files_and_dirs = chain(
        *[dirnames + filenames for _, dirnames, filenames in os.walk(path)])

    hidden = [
        f for f in files_and_dirs if f.startswith('.')
        if f not in {'.gitkeep', '.gitignore'}
    ]

    assert not hidden

    # check template directories
    dirs = ['doc', 'exploratory', 'lib', 'products', 'src', 'tests']
    assert all([(path / dir_).exists() for dir_ in dirs])
