import os
import shutil
import subprocess
from pathlib import Path

import yaml
import pytest

from ploomber.cli import install
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
    Configures environment. This takes a while, to re-use existing conda env
    call: pytest --cache-env
    """
    tmp_target = tmp_path_factory.mktemp('session-wide-tmp-directory')

    old = os.getcwd()
    os.chdir(tmp_target)

    scaffold.cli(project_path='my_new_project', conda=False, package=True)
    os.chdir('my_new_project')

    egg_info = Path('src', 'package_name.egg-info')

    if egg_info.exists():
        shutil.rmtree(egg_info)

    if request.config.getoption("--cache-env"):
        print('Using cached env...')
    else:
        install.main()

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


def test_wheel_layout(setup_env):
    run("""
    source venv-my_new_project/bin/activate
    pip install wheel
    rm -rf dist/ build/
    python setup.py bdist_wheel
    cd dist
    unzip *.whl
    """)

    assert Path('dist/my_new_project/pipeline.yaml').is_file()


def test_pytest(setup_env):
    script = """
    source venv-my_new_project//bin/activate
    pytest
    """
    Path('test.sh').write_text(script)

    assert not subprocess.run(['bash', 'test.sh']).returncode


def test_ploomber_build(setup_env):
    assert not run("""
    source venv-my_new_project//bin/activate
    ploomber build
    """)


def test_ploomber_status_from_wheel(setup_env):
    assert not run("""
    source venv-my_new_project/bin/activate
    pip install wheel
    pip uninstall my_new_project --yes
    rm -rf dist/ build/
    python setup.py bdist_wheel
    pip install dist/*
    ploomber status
    """)


def test_exploratory_notebook(setup_env):
    assert not run("""
    source venv-my_new_project/bin/activate
    jupyter nbconvert --to notebook --execute exploratory/example.ipynb
    """)


def test_versioneer_configured(setup_env):
    assert not run('python setup.py version')


def test_conda(tmp_directory):
    """
    Instead of running the same tests with conda (takes too long), we check the
    environments are equivalent
    """
    scaffold.cli(project_path='with_conda', conda=True, package=True)
    scaffold.cli(project_path='with_pip', conda=False, package=True)

    def _get_deps_from_env(name):
        env = yaml.safe_load(Path('with_conda', name).read_text())
        return set(env['dependencies'][-1]['pip'])

    def _get_deps_from_reqs(name):
        lines = Path('with_pip', name).read_text().splitlines()
        return set(line for line in lines if not line.startswith('#'))

    env = _get_deps_from_env('environment.yml')
    env_dev = _get_deps_from_env('environment.dev.yml')

    req = _get_deps_from_reqs('requirements.txt')
    req_dev = _get_deps_from_reqs('requirements.dev.txt')

    assert env == req
    assert env_dev == req_dev


@pytest.mark.parametrize('conda', [True, False])
def test_check_layout(tmp_directory, conda):
    scaffold.cli(project_path='myproj', conda=conda, package=True)
    os.chdir('myproj')
    assert Path('src/myproj/pipeline.yaml').is_file()


@pytest.mark.parametrize('conda', [True, False])
def test_readme_includes_pip_install_command(tmp_directory, conda):
    scaffold.cli(project_path='myproj', conda=conda, package=True)
    os.chdir('myproj')
    readme = Path('README.md').read_text()

    assert 'pip install --editable .' in readme
