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

## Distribution

TODO: add changelog edit git tag instructions

To generate an arifact for deployment:

```
bash distribute/main/build.sh

# for help
bash distribute/main/build.sh --help
```

`build.sh` creates a [wheel](https://packaging.python.org/glossary/) from the package and zips ti along with the `environment.yml`, `setup.sh` and `Procfile`.

## Deployment


Although the usual `pip install {wheel}.whl` is supported, this project has non-Python dependencies that are better handled via `conda`, the recommended installation procedure is as follows:

```
# unzip the file generated in the previous step
unzip dist-main.zip
cd dist-main/

# create conda environment and install all dependencies
bash setup.sh
```

After setting up, the application is ready to run. `Procfile` states the commands needed to start the application.


