import os
import subprocess
from pathlib import Path

from ploomber_scaffold import scaffold


def test_cli(tmp_directory):
    scaffold.cli(project_path='my_new_project')
    os.chdir('my_new_project')

    # setup command
    assert not subprocess.run(['invoke', 'setup']).returncode

    # test command
    script = """
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    invoke test --inplace
    """
    Path('test.sh').write_text(script)

    assert not subprocess.run(['bash', 'test.sh']).returncode

    # test run pipeline
    script = """
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    ploomber build
    """
    Path('build.sh').write_text(script)

    assert not subprocess.run(['bash', 'build.sh']).returncode

    # test installing from wheel
    script = """
    eval "$(conda shell.bash hook)"
    conda activate my_new_project
    pip uninstall my_new_project --yes
    python setup.py bdist_wheel
    pip install dist/my_new_project-0.1.dev0-py3-none-any.whl
    ploomber build
    """
    Path('build_from_wheel.sh').write_text(script)

    assert not subprocess.run(['bash', 'build_from_wheel.sh']).returncode
