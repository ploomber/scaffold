import os
from pathlib import Path
from unittest.mock import Mock, _Call
from datetime import datetime

import pytest

from versioneer import Versioner
import versioneer


# FIXME: use unittest.mock.call instead of unittest.mock._Call
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
    ['0.9', '0.9.1dev'],
])
def test_bump_up_version(monkeypatch, version, version_new, move_to_project):
    monkeypatch.setattr(Versioner, 'current_version', lambda self: version)
    assert Versioner().bump_up_version() == version_new


def test_commit_version_no_tag(backup_template, monkeypatch):
    v = Versioner()

    mock = Mock()
    monkeypatch.setattr(versioneer, 'call', mock)

    v.commit_version('0.2',
                     msg_template='{package_name} release {new_version}',
                     tag=False)

    assert mock.call_args_list == [
        _call(['git', 'add', '--all']),
        _call(['git', 'status']),
        _call(['git', 'commit', '-m', 'package_name release 0.2']),
    ]

    assert "__version__ = '0.2'" in (v.PACKAGE / '__init__.py').read_text()


def test_commit_version_tag(backup_template, monkeypatch):
    v = Versioner()

    mock = Mock()
    monkeypatch.setattr(versioneer, 'call', mock)

    v.commit_version('0.2',
                     msg_template='{package_name} release {new_version}',
                     tag=True)

    assert mock.call_args_list == [
        _call(['git', 'add', '--all']),
        _call(['git', 'status']),
        _call(['git', 'commit', '-m', 'package_name release 0.2']),
        _call(['git', 'tag', '-a', '0.2', '-m', 'package_name release 0.2']),
        _call(['git', 'push', 'origin', '0.2'])
    ]

    assert "__version__ = '0.2'" in (v.PACKAGE / '__init__.py').read_text()


def test_update_changelog_release_md(backup_template):
    v = Versioner()
    v.update_changelog_release('0.1')
    today = datetime.now().strftime('%Y-%m-%d')
    assert v.path_to_changelog.read_text(
    ) == f'# CHANGELOG\n\n## 0.1 ({today})'


def test_update_changelog_release_rst(backup_template):
    Path('CHANGELOG.md').unlink()
    Path('CHANGELOG.rst').write_text('CHANGELOG\n=========\n\n0.1dev\n------')

    v = Versioner()
    v.update_changelog_release('0.1')
    today = datetime.now().strftime('%Y-%m-%d')
    assert v.path_to_changelog.read_text(
    ) == f'CHANGELOG\n=========\n\n0.1 ({today})\n----------------'


def test_add_changelog_new_dev_section_md(backup_template):
    v = Versioner()
    v.add_changelog_new_dev_section('0.2dev')
    assert v.path_to_changelog.read_text(
    ) == '# CHANGELOG\n\n## 0.2dev\n\n## 0.1dev'


def test_add_changelog_new_dev_section_rst(backup_template):
    Path('CHANGELOG.md').unlink()
    Path('CHANGELOG.rst').write_text('CHANGELOG\n=========\n\n0.1dev\n------')

    v = Versioner()
    v.add_changelog_new_dev_section('0.2dev')
    assert v.path_to_changelog.read_text(
    ) == 'CHANGELOG\n=========\n\n0.2dev\n------\n\n0.1dev\n------'


def test_release(backup_template, monkeypatch):
    mock = Mock()
    mock_input = Mock()
    mock_input.side_effect = ['', 'y']

    monkeypatch.setattr(versioneer, 'call', mock)
    monkeypatch.setattr(versioneer, '_input', mock_input)

    versioneer.version(tag=True)

    assert mock.call_args_list == [
        _call(['git', 'add', '--all']),
        _call(['git', 'status']),
        _call(['git', 'commit', '-m', 'package_name release 0.1']),
        _call(['git', 'tag', '-a', '0.1', '-m', 'package_name release 0.1']),
        _call(['git', 'push', 'origin', '0.1']),
        _call(['git', 'add', '--all']),
        _call(['git', 'status']),
        _call([
            'git', 'commit', '-m', 'Bumps up package_name to version 0.1.1dev'
        ]),
        _call(['git', 'push'])
    ]

    today = datetime.now().strftime('%Y-%m-%d')
    assert Path('CHANGELOG.md').read_text(
    ) == f'# CHANGELOG\n\n## 0.1.1dev\n\n## 0.1 ({today})'


def test_release_with_no_changelog(backup_template, monkeypatch, capsys):
    Path('CHANGELOG.md').unlink()

    mock = Mock()
    mock_input = Mock()
    mock_input.side_effect = ['', 'y']

    monkeypatch.setattr(versioneer, 'call', mock)
    monkeypatch.setattr(versioneer, '_input', mock_input)

    versioneer.version(tag=True)

    captured = capsys.readouterr()
    assert ('No CHANGELOG.{rst,md} found, skipping changelog editing...'
            in captured.out)

    assert mock.call_args_list == [
        _call(['git', 'add', '--all']),
        _call(['git', 'status']),
        _call(['git', 'commit', '-m', 'package_name release 0.1']),
        _call(['git', 'tag', '-a', '0.1', '-m', 'package_name release 0.1']),
        _call(['git', 'push', 'origin', '0.1']),
        _call(['git', 'add', '--all']),
        _call(['git', 'status']),
        _call([
            'git', 'commit', '-m', 'Bumps up package_name to version 0.1.1dev'
        ]),
        _call(['git', 'push'])
    ]


@pytest.mark.parametrize('production', [False, True])
def test_upload(backup_template, monkeypatch, production):
    mock = Mock()
    mock_input = Mock()
    mock_input.side_effect = ['y']

    monkeypatch.setattr(versioneer, 'call', mock)
    monkeypatch.setattr(versioneer, '_input', mock_input)

    versioneer.upload(tag='0.1', production=production)

    upload_call = (_call(['twine', 'upload', 'dist/*'])
                   if production else _call([
                       'twine', 'upload', '--repository-url',
                       'https://test.pypi.org/legacy/', 'dist/*'
                   ]))

    assert mock.call_args_list == [
        _call(['git', 'checkout', '0.1']),
        _call(['rm', '-rf', 'dist/', 'build/']),
        _call(['python', 'setup.py', 'bdist_wheel']),
        upload_call,
    ]
