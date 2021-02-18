"""
Test invoke commands
"""
from pathlib import Path
import os
from unittest.mock import Mock, call
import importlib

import pytest
from invoke import MockContext, Result

import tasks


def test_version(monkeypatch):
    m = Mock()
    monkeypatch.setattr(tasks.versioneer, 'version', m)

    tasks.version(MockContext())

    m.assert_called_with(project_root='.', tag=True)


def test_invoke_test_with_nox(monkeypatch):
    c = MockContext(run=Result())
    tasks.test(c)

    c.run.assert_called_with('nox', pty=True)


@pytest.fixture
def move_to_template():
    original = os.getcwd()

    os.chdir('src/ploomber_scaffold/template')

    yield

    os.chdir(original)


@pytest.fixture
def create():
    Path('environment.lock.yml').touch()

    yield True

    Path('environment.lock.yml').unlink()


@pytest.fixture
def do_nothing():
    return False


@pytest.fixture(params=['create', 'do_nothing'])
def create_lock_file(request):
    return request.getfixturevalue(request.param)


def test_noxfile(move_to_template, create_lock_file):
    import noxfile
    importlib.reload(noxfile)

    expected = ('environment.lock.yml'
                if create_lock_file else 'environment.yml')

    session = Mock()
    noxfile.tests(session=session)

    # install dependencies
    session._run.assert_called_with('conda', 'env', 'update', '--prefix',
                                    session.virtualenv.location, '--file',
                                    expected)

    session.install.assert_called_with('--editable', '.[dev]')

    # run tests and generate lock file
    session.run.assert_has_calls([
        call('pytest', 'tests/'),
        call('conda', 'env', 'export', '--prefix', session.virtualenv.location,
             '--file', 'environment.lock.yml')
    ])

    # lock file does not exist yet, should default to this one...
    assert noxfile.env_file == expected
