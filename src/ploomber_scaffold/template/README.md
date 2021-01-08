# package_name

Requires [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

## Setup development environment

```sh
pip installl invoke

# install dependencies
invoke setup

# activate environment
conda activate package_name
```

## Testing

```sh
# creates a fresh virtual environment
invoke test

# ...or to run tests in the current environment
invoke test --inplace
```

## Running the pipeline

```sh
ploomber build

# ..or to start an interactive session
ploomber interact
```

## Exporting to Kubernetes or Airflow

If you want to export to Airflow or Kubernetes, add "soopervisor" to your
dependencies and check out the docs: https://soopervisor.readthedocs.io/

```sh
# export to kubernetes/argo
soopervisor export

# export to airflow
soopervisor export-airflow
```
