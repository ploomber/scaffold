import os
from pathlib import Path
from unittest.mock import Mock, _Call
from datetime import datetime

import pytest

from versioneer import Versioner
import versioneer


def _call(arg):
    """Shortcut for comparing call objects
    """
    return _Call(((arg, ), ))


@pytest.fixture
def move_to_project():
    old = os.getcwd()
    p = Path('src', 'ploomber_scaffold', 'template')
    os.chdir(p)
    yield
    os.chdir(old)


def test_locate_package_and_readme(move_to_project):
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


def test_commit_version_no_tag(backup_template, monkeypatch):
    v = Versioner()

    mock = Mock()
    monkeypatch.setattr(versioneer, 'call', mock)

    v.commit_version('0.2', tag=False)

    assert mock.call_args_list == [
        _call(['git', 'add', '--all']),
        _call(['git', 'status']),
        _call(['git', 'commit', '-m', 'Release 0.2']),
    ]

    assert "__version__ = '0.2'" in (v.PACKAGE / '__init__.py').read_text()


def test_commit_version_tag(backup_template, monkeypatch):
    v = Versioner()

    mock = Mock()
    monkeypatch.setattr(versioneer, 'call', mock)

    v.commit_version('0.2', tag=True)

    assert mock.call_args_list == [
        _call(['git', 'add', '--all']),
        _call(['git', 'status']),
        _call(['git', 'commit', '-m', 'Release 0.2']),
        _call(['git', 'tag', '-a', '0.2', '-m', 'package_name release 0.2']),
        _call(['git', 'push', 'origin', '0.2'])
    ]

    assert "__version__ = '0.2'" in (v.PACKAGE / '__init__.py').read_text()


def test_update_changelog_release(backup_template):
    v = Versioner()
    v.update_changelog_release('0.1')
    today = datetime.now().strftime('%Y-%m-%d')
    assert v.path_to_changelog.read_text(
    ) == f'# CHANGELOG\n\n## 0.1 ({today})'


def test_add_changelog_new_dev_section(backup_template):
    v = Versioner()
    v.add_changelog_new_dev_section('0.2dev')
    assert v.path_to_changelog.read_text(
    ) == '# CHANGELOG\n\n## 0.2dev\n\n## 0.1dev'
