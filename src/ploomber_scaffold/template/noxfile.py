"""
nox configuration file.
docs: https://nox.thea.codes/en/stable/index.html
"""
import sys
from pathlib import Path

import nox


def env_file_name():
    """
    Get environment file to use, prioritizing environment.lock.yml
    """
    env_file = 'environment.lock.yml'

    if not Path(env_file).exists():
        print('[WARNING] environment.lock.yaml does not '
              'exist, looking for environment.yml...')

        env_file = 'environment.yml'

        if not Path(env_file).exists():
            print('[ERROR] No conda environment file found. Aborting.')
            sys.exit(1)
        else:
            print('Using environment.yml...')

    return env_file


env_file = env_file_name()


@nox.session(venv_backend='conda', python='3.8')
def tests(session):
    session._run('conda', 'env', 'update', '--prefix',
                 session.virtualenv.location, '--file', env_file)

    session.install('--editable', '.[dev]')

    session.run('pytest', 'tests/')

    print('Generating environment.lock.yml...')
    session.run('conda', 'env', 'export', '--prefix',
                session.virtualenv.location, '--file', 'environment.lock.yml')
