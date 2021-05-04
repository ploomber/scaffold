# package_name

Requires [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

## Setup development environment

```sh
# configure dev environment
ploomber install

# activate conda environment
conda activate package_name
```

## Testing

```sh
pytest
```

## Running the pipeline

```sh
ploomber build

# start an interactive session
ploomber interact
```

## Exporting to other systems

[soopervisor](https://soopervisor.readthedocs.io/) allows you to run ploomber projects in other environments. Check out the docs to learn more.
