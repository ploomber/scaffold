"""
nox docs: https://nox.thea.codes/en/stable/index.html

NOTE: add python="3.x" to nox.session to test against a specific version
"""
import nox

# TODO: configure from environment.yml
@nox.session(venv_backend='conda')
def tests(session):
    session.install('.[test]')
    session.run('pytest')
