import papermill as pm
import pytest

from pathlib import Path

path_to_exploratory = Path(__file__).parents[1] / 'exploratory'
path_to_exploratory_tests = Path(__file__).parents[1] / 'exploratory-tests'


@pytest.mark.parametrize(
    'name',
    [
        'example.ipynb',
        # other notebooks...
    ])
def test_exploratory(name):
    """
    Smoke tests for notebooks in exploratory/ (runs the noteboks but does not
    check output)
    """
    path_to_exploratory_tests.mkdir(exist_ok=True)

    pm.execute_notebook(path_to_exploratory / name,
                        path_to_exploratory_tests / name)
