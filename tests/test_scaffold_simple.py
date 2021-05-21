import shutil
import os
import subprocess
from pathlib import Path

import pytest

from ploomber_scaffold import scaffold
from ploomber.cli import install


def run(script):
    """Run a script and return its returncode
    """
    Path('script.sh').write_text(script)
    return subprocess.run(['bash', 'script.sh'], check=True).returncode


@pytest.fixture(scope='module')
def setup_env(request, tmp_path_factory):
    """
    Configures environment. This takes a while, to re-use existing conda env
    call: pytest --cache-env
    """
    tmp_target = tmp_path_factory.mktemp('session-wide-tmp-simple')

    old = os.getcwd()
    os.chdir(tmp_target)

    scaffold.cli(project_path='my_simple_project', conda=False, package=False)
    os.chdir('my_simple_project')

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


def test_check_layout(setup_env):
    assert Path('pipeline.yaml').is_file()


def test_ploomber_build(setup_env):
    assert not run("""
    source venv-my_simple_project//bin/activate
    ploomber build
    """)
