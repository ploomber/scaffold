"""
Common tests for simple and package versions
"""
import os
from pathlib import Path
from unittest.mock import Mock

import pytest

from ploomber_scaffold import scaffold
from ploomber_scaffold.exceptions import ScaffoldError


def _path_str(s):
    return str(Path(s))


@pytest.mark.parametrize('conda, package, deps, dev_deps, expected_pipeline', [
    [
        False,
        False,
        _path_str('myproj/requirements.txt'),
        _path_str('myproj/requirements.dev.txt'),
        _path_str('myproj/pipeline.yaml'),
    ],
    [
        False,
        True,
        _path_str('myproj/requirements.txt'),
        _path_str('myproj/requirements.dev.txt'),
        _path_str('myproj/src/myproj/pipeline.yaml'),
    ],
    [
        True,
        False,
        _path_str('myproj/environment.yml'),
        _path_str('myproj/environment.dev.yml'),
        _path_str('myproj/pipeline.yaml'),
    ],
    [
        True,
        True,
        _path_str('myproj/environment.yml'),
        _path_str('myproj/environment.dev.yml'),
        _path_str('myproj/src/myproj/pipeline.yaml'),
    ],
])
def test_output_message(tmp_directory, capsys, conda, package, deps, dev_deps,
                        expected_pipeline):
    scaffold.cli(project_path='myproj', conda=conda, package=package)
    captured = capsys.readouterr()

    assert f'Pipeline declaration: {expected_pipeline}' in captured.out
    assert f'Add deployment dependencies to {deps}' in captured.out
    assert f'Add development dependencies to {dev_deps}' in captured.out


@pytest.mark.parametrize('package', [True, False])
def test_with_conda(tmp_directory, package):
    scaffold.cli(project_path='myproj', conda=True, package=package)
    os.chdir('myproj')
    readme = Path('README.md').read_text()
    conda_msg = ('# activate conda environment\n' 'conda activate myproj')

    assert 'conda env create --file environment.yml' in readme
    assert 'Requires [Miniconda]' in readme
    assert conda_msg in readme


@pytest.mark.parametrize('package', [True, False])
def test_with_pip(tmp_directory, package):
    scaffold.cli(project_path='myproj', conda=False, package=package)
    os.chdir('myproj')
    readme = Path('README.md').read_text()

    assert 'Requires [Miniconda]' not in readme
    assert 'python -m venv {path-to-venv}' in readme
    assert 'source {path-to-venv}/bin/activate' in readme


def test_empty_no_package(tmp_directory):
    scaffold.cli(project_path='myproj', conda=False, package=False, empty=True)

    expected = (
        'tasks:\n  # Add tasks here...\n\n  # Example\n  # - '
        'source: path/to/script.py\n  #   product: products/report.ipynb\n')
    assert not Path('myproj', 'tasks').exists()
    assert not Path('myproj', 'scripts').exists()
    assert Path('myproj', 'pipeline.yaml').read_text() == expected


def test_empty_package(tmp_directory):
    scaffold.cli(project_path='myproj', conda=False, package=True, empty=True)

    expected = ('meta:\n  # paths in task sources (e.g., scripts/fit.py)'
                ' are relative to src/package_name\n  source_loader:\n    '
                'module: package_name\n\ntasks:\n  # Add tasks here...\n\n  '
                '# Example\n  # - source: scripts/fit.py\n  #   product: '
                'products/report.ipynb\n')

    pkg_root = Path('myproj', 'src', 'myproj')
    assert not Path(pkg_root, 'tasks').exists()
    assert not Path(pkg_root, 'scripts').exists()
    assert Path(pkg_root, 'pipeline.yaml').read_text() == expected


@pytest.mark.parametrize('name, package', [
    ['my-project', False],
    ['my_project', True],
])
def test_accepts_dashes_if_non_package(tmp_directory, name, package):
    scaffold.cli(project_path=name, conda=False, package=package, empty=True)


def test_rejects_dashes_if_package(tmp_directory):
    with pytest.raises(ScaffoldError) as excinfo:
        scaffold.cli(project_path='my-project',
                     conda=False,
                     package=True,
                     empty=True)

    assert 'is not a valid package identifier' in str(excinfo.value)


def test_doesnt_show_instructions_if_name_passed(monkeypatch, tmp_directory):
    mock = Mock()
    monkeypatch.setattr(scaffold, '_echo_instructions', mock)

    scaffold.cli(project_path='my-project',
                 conda=False,
                 package=False,
                 empty=True)

    mock.assert_not_called()
