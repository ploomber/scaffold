"""
nox docs: https://nox.thea.codes/en/stable/index.html
"""
import nox
import yaml

# read python version dependency declared in environment.yml
with open('environment.yml') as f:
    env_yml = yaml.load(f, Loader=yaml.SafeLoader)

py_dep = [dep for dep in env_yml['dependencies']
          if dep.startswith('python=3.')]

if not len(py_dep):
    raise RuntimeError('environment.yml should declare python=3.x as '
                       'dependency')
if len(py_dep) > 1:
    raise RuntimeError('More than one python=3.x dependency declared')

py_version = py_dep[0].split('=')[1]


@nox.session(venv_backend='conda', python=py_version)
def tests(session):
    # install package along with test requirements
    session.install('.[test]')
    # run tests
    session.run('pytest')
