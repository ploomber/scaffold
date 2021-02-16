from ploomber.executors import Serial
from ploomber.spec import DAGSpec


def test_pipeline():
    """
    This is a smoke test, checking that the pipeline runs (but not the output)

    NOTE: it's common for pipelines to take hours to run, a way to make this
    test feasible is to run it here with a sample of the data and save results
    in a different folder to prevent overwriting your results.
    """
    # load dag
    dag = DAGSpec.find().to_dag()

    # change executor settings: you can use "pytest --pdb" to start a debugging
    # session if the test fails. Calling dag['task'].debug() is another
    # option
    dag.executor = Serial(build_in_subprocess=False, catch_exceptions=False)

    # a third approach for debugging is to use: import IPython; IPython.embed()
    # to start an interactive session at this point. To do so, you must call
    # "pytest -s"

    dag.build()
