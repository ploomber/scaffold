import os


def run_in_env(c, command, env):
    commands = [
        'eval "$(conda shell.bash hook)"' if os.name == 'posix' else '',
        f'conda activate {env}'
    ]
    commands.append(command)
    c.run(' && '.join(commands))
