import shutil
import tempfile
import os
import sys
from pathlib import Path

import pytest

# add template/lib to path, we'll be testing those files
root = Path(__file__).parent.parent
sys.path.append(str(root / 'src' / 'ploomber_scaffold' / 'template'))
sys.path.append(str(root / 'src' / 'ploomber_scaffold' / 'template' / 'lib'))


@pytest.fixture()
def tmp_directory(tmp_path):
    old = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(old)


@pytest.fixture
def backup_template():
    old = os.getcwd()
    backup = tempfile.mkdtemp()
    backup_template = str(Path(backup, 'backup-template'))
    path_to_templates = root / 'src' / 'ploomber_scaffold' / 'template'
    shutil.copytree(str(path_to_templates), backup_template)

    os.chdir(path_to_templates)

    yield path_to_templates

    os.chdir(old)

    shutil.rmtree(str(path_to_templates))
    shutil.copytree(backup_template, str(path_to_templates))
    shutil.rmtree(backup)
