import os
import subprocess
from pathlib import Path

import pytest

from ploomber_scaffold import scaffold


def run(script):
    """Run a script and return its returncode
    """
    Path('script.sh').write_text(script)
    return subprocess.run(['bash', 'script.sh']).returncode


@pytest.mark.parametrize('name, valid', [
    ('project', True),
    ('project123', True),
    ('pro_jec_t', True),
    ('pro-ject', False),
    ('1234', False),
    ('a project', False),
])
def test_is_valid_package_name(name, valid):
    assert scaffold.is_valid_package_name(name) is valid


@pytest.fixture(scope='module')
def setup_env(tmp_path_factory):
    tmp_target = tmp_path_factory.mktemp('session-wide-tmp-directory')

    old = os.getcwd()
    os.chdir(tmp_target)

    scaffold.cli(project_path='my_new_project')
    os.chdir('my_new_project')
    subprocess.run(['invoke', 'setup'], check=True)

    # versioneer depends on this
    run("""
    git init
    git add --all
    git commit -m 'my first commit'
    """)

    yield tmp_target

    os.chdir(old)


def test_invoke_test(setup_env):
    script = """
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    invoke test --inplace
    """
    Path('test.sh').write_text(script)

    assert not subprocess.run(['bash', 'test.sh']).returncode


def test_ploomber_build(setup_env):
    assert not run("""
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    ploomber build
    """)


def test_ploomber_build_from_wheel(setup_env):
    assert not run("""
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    pip uninstall my_new_project --yes
    rm -rf dist/ build/
    python setup.py bdist_wheel
    pip install dist/*
    ploomber build
    """)


def test_exploratory_notebook(setup_env):
    assert not run("""
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    jupyter nbconvert --to notebook --execute exploratory/example.ipynb
    """)


def test_versioneer_configured(setup_env):
    assert not run('python setup.py version')
