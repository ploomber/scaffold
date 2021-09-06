import os
import shutil
from pathlib import Path

import yaml
import pytest

from ploomber.cli import install
from ploomber_scaffold import scaffold
from utils import run, activate_cmd


@pytest.fixture
def clean_dist():
    if Path('dist').exists():
        shutil.rmtree('dist')

    if Path('build').exists():
        shutil.rmtree('build')


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
        install.main(use_lock=False)

    # versioneer depends on this
    run("""
    git init
    git config user.email "you@example.com"
    git config user.name "Your Name"
    git add --all
    git commit -m "my first commit"
    """)

    yield tmp_target

    os.chdir(old)


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


def test_wheel_layout(setup_env, clean_dist):
    run(f"""
    {activate_cmd('venv-my_new_project')}
    pip install wheel
    python setup.py bdist_wheel
    """)

    filename = os.listdir('dist')[0]
    shutil.unpack_archive(str(Path('dist', filename)), 'dist', format='zip')

    assert Path('dist/my_new_project/pipeline.yaml').is_file()


def test_pytest(setup_env):
    assert not run(f"""
    {activate_cmd('venv-my_new_project')}
    pytest
    """)


def test_ploomber_build(setup_env):
    assert not run(f"""
    {activate_cmd('venv-my_new_project')}
    ploomber build
    """)


def test_ploomber_status_from_wheel(setup_env, clean_dist):
    assert not run(f"""
    {activate_cmd('venv-my_new_project')}
    pip install wheel
    pip uninstall my_new_project --yes
    python setup.py bdist_wheel
    """)

    dist_path = str(Path('dist', os.listdir('dist')[0]))

    assert not run(f"""
    {activate_cmd('venv-my_new_project')}
    pip install {dist_path}
    ploomber status
    """)


def test_exploratory_notebook(setup_env):
    assert not run(f"""
    {activate_cmd('venv-my_new_project')}
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
