from invoke import run


def test_help():
    result = run('cd template/ && bash setup.sh --help', hide=True)
    assert result.ok


def test_setup_sh():
    result = run('cd template/ && bash setup.sh some_env', hide=True)
    assert result.ok

    # check env was created
    result = run('conda env list | grep some_env', hide=True)
    assert 'some_env' in result.stdout

    # delete env
    result = run('conda remove --name some_env --all --yes', hide=True)
    assert result.ok
