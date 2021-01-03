import os
from pathlib import Path

import pytest

from versioneer import Versioner


@pytest.fixture
def move_to_project():
    old = os.getcwd()
    p = Path('src', 'ploomber_scaffold', 'template')
    os.chdir(p)
    yield
    os.chdir(old)


def test_locate_package_and_readme():
    v = Versioner()
    assert v.PACKAGE == Path('src', 'package_name')
    assert v.path_to_changelog == Path('CHANGELOG.md')


def test_current_version(move_to_project):
    assert Versioner().current_version() == '0.1dev'


def test_release_version(move_to_project):
    assert Versioner().release_version() == '0.1'


@pytest.mark.parametrize('version, version_new', [
    ['0.1', '0.1.1dev'],
    ['0.1.1', '0.1.2dev'],
])
def test_bump_up_version(monkeypatch, version, version_new, move_to_project):
    monkeypatch.setattr(Versioner, 'current_version', lambda self: version)
    assert Versioner().bump_up_version() == version_new


def test_commit_version(backup_template):
    v = Versioner()
