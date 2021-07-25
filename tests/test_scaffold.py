"""
Common tests for simple and package versions
"""
import os
from pathlib import Path

import pytest

from ploomber_scaffold import scaffold


@pytest.mark.parametrize('conda, package, deps, dev_deps, expected_pipeline', [
    [
        False,
        False,
        'myproj/requirements.txt',
        'myproj/requirements.dev.txt',
        'myproj/pipeline.yaml',
    ],
    [
        False,
        True,
        'myproj/requirements.txt',
        'myproj/requirements.dev.txt',
        'myproj/src/myproj/pipeline.yaml',
    ],
    [
        True,
        False,
        'myproj/environment.yml',
        'myproj/environment.dev.yml',
        'myproj/pipeline.yaml',
    ],
    [
        True,
        True,
        'myproj/environment.yml',
        'myproj/environment.dev.yml',
        'myproj/src/myproj/pipeline.yaml',
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
        'source: path/to/script.py\n  #   product: products/report.html\n')
    assert not Path('myproj', 'tasks').exists()
    assert not Path('myproj', 'scripts').exists()
    assert Path('myproj', 'pipeline.yaml').read_text() == expected


def test_empty_package(tmp_directory):
    scaffold.cli(project_path='myproj', conda=False, package=True, empty=True)

    expected = ('meta:\n  # paths in task sources (e.g., scripts/fit.py)'
                ' are relative to src/package_name\n  source_loader:\n    '
                'module: package_name\n\ntasks:\n  # Add tasks here...\n\n  '
                '# Example\n  # - source: scripts/fit.py\n  #   product: '
                'products/report.html\n')

    pkg_root = Path('myproj', 'src', 'myproj')
    assert not Path(pkg_root, 'tasks').exists()
    assert not Path(pkg_root, 'scripts').exists()
    assert Path(pkg_root, 'pipeline.yaml').read_text() == expected
