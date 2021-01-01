import nox


@nox.session(venv_backend='conda', python='3.8')
def tests(session):
    session.install('--editable', '.[dev]')
    session.run('pytest', 'tests/')
