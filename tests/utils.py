import os
import subprocess
import sys
from pathlib import Path


def run(script, raise_=False):
    """Run a script and return its returncode
    """
    Path('script.sh' if os.name == 'posix' else 'script.bat').write_text(
        script)
    cmd = ['bash', 'script.sh'] if os.name == 'posix' else ['script.bat']

    code = subprocess.run(cmd, check=True).returncode

    if code and raise_:
        raise RuntimeError(f'Failed to execute: {script}')

    return code


def activate_cmd(path):
    """
    Returns a command to activate the environment

    pywin32 breaks jupyter on windows, this command ensures that the venv
    has a version that works. I tried moving the pywin32 installation part
    to the setup_env fixtures so the installation only happens once but
    started to get some errors. So this will uninstall/install on each
    tests slowing things down a bit but it works.
    """
    # Reference
    # https://github.com/jupyter/notebook/issues/4980
    # https://github.com/mhammond/pywin32/issues/1409

    # jupyter will remove pywin32 in an upcoming version
    # https://github.com/jupyter/jupyter_core/pull/230
    if os.name == 'nt':
        pywin32_v = '224' if sys.version_info < (3, 8) else '225'
        return f"""
call {path}\\Scripts\\activate.bat
pip uninstall pywin32 --yes
pip install pywin32=={pywin32_v}
python {path}\\Scripts\\pywin32_postinstall.py -install
"""
    else:
        return f'source {path}/bin/activate'
