import os
import subprocess
from pathlib import Path

import pytest

from ploomber_scaffold import scaffold


def run(script):
    """Run a script and return its returncode
    """
    Path('script.sh').write_text(script)
    return subprocess.run(['bash', 'script.sh'], check=True).returncode


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
def setup_env(request, tmp_path_factory):
    """
    Configures environment. This takes a while, to re-use existing env
    call: pytest --cache-env
    """
    tmp_target = tmp_path_factory.mktemp('session-wide-tmp-directory')

    old = os.getcwd()
    os.chdir(tmp_target)

    scaffold.cli(project_path='my_new_project')
    os.chdir('my_new_project')

    if request.config.getoption("--cache-env"):
        print('Using cached env...')
    else:
        subprocess.run(['invoke', 'setup'], check=True)

    # versioneer depends on this
    run("""
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
    git add --all
    git commit -m 'my first commit'
    """)

    yield tmp_target

    os.chdir(old)


def test_check_layout(setup_env):
    assert Path('src/my_new_project/pipeline.yaml').is_file()
    assert Path('src/my_new_project/pipeline-features.yaml').is_file()


def test_wheel_layout(setup_env):
    run("""
    rm -rf dist/ build/
    python setup.py bdist_wheel
    cd dist
    unzip *.whl
    """)

    assert Path('dist/my_new_project/pipeline.yaml').is_file()
    assert Path('dist/my_new_project/pipeline-features.yaml').is_file()


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
    python -m build --wheel .
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
