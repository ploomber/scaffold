import os
import sys
from pathlib import Path

import pytest

# add template/lib to path, we'll be testing those files
root = Path(__file__).parent.parent
sys.path.append(str(root / 'src' / 'ploomber_scaffold' / 'template' / 'lib'))


@pytest.fixture()
def tmp_directory(tmp_path):
    old = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(old)
