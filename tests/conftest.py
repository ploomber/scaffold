import os
import sys
from pathlib import Path

import pytest

_root = Path(__file__).parent.parent
sys.path.append(str(_root / 'src' / 'ploomber_scaffold' / 'template'))


@pytest.fixture
def root():
    return Path(_root)


@pytest.fixture
def tmp_directory(tmp_path):
    old = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(old)


def pytest_addoption(parser):
    parser.addoption("--cache-env", action="store_true")
