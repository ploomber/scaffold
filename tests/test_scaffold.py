import pytest

from ploomber_scaffold import scaffold


@pytest.mark.parametrize('conda, package, deps, dev_deps, expected_pipeline', [
    [
        False,
        False,
        'myproj/requirements.txt',
        'myproj/requirements.dev.txt',
        'myproj/pipeline.yaml',
    ],
    [
        False,
        True,
        'myproj/requirements.txt',
        'myproj/requirements.dev.txt',
        'myproj/src/myproj/pipeline.yaml',
    ],
    [
        True,
        False,
        'myproj/environment.yml',
        'myproj/environment.dev.yml',
        'myproj/pipeline.yaml',
    ],
    [
        True,
        True,
        'myproj/environment.yml',
        'myproj/environment.dev.yml',
        'myproj/src/myproj/pipeline.yaml',
    ],
])
def test_output_message(tmp_directory, capsys, conda, package, deps, dev_deps,
                        expected_pipeline):
    scaffold.cli(project_path='myproj', conda=conda, package=package)
    captured = capsys.readouterr()

    assert f'Pipeline declaration: {expected_pipeline}' in captured.out
    assert f'Add deployment dependencies to {deps}' in captured.out
    assert f'Add development dependencies to {dev_deps}' in captured.out
