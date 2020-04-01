# package_name

TODO:
1. Modify `environment.yml` with your supported Python version
2. Review dependencies to install via conda
3. Install conda environment `conda env create -f environment.yml`
4. Activate environment `conda activate package_name`
5. Install your package in editable mode, with all depdencies inside the conda environment `pip install --editable ".[all]"`
6. [add data files to gitignore] but let the user decide

## Setup development environment

Once you cloned the repo:

```sh
# this will create a conda env called "package_name", will replace
# an existing one if any
conda env create --file environment.yml --force

# install the package in editable mode to reflect source code changes
pip install --editable ".[all]"

# test installation
pytest
```

For running tests you also need: `pip install ".[test]"`

For building documentation: `pip install ".[doc]"`


## Testing

(`conda` is required)

```
nox
```


## Distribution

TODO: add changelog edit git tag instructions

To generate a [wheel](https://packaging.python.org/glossary/) use the standard command:

```
python setup.py bdist_wheel
```

After generating the wheel, update it by adding the `environment.yml` file:

```
zip -u dist/{wheel_name}.whl environment.yml
```

### Installing from a wheel

Although the usual `pip install {wheel}.whl` is supported, this project has non-Python dependencies that are better handled via `conda`, the recommended installation procedure is as follows:

```
# extract environment.yml
unzip -p {wheel}.whl environment.yml > environment.yml

# create conda environment
conda env create -f environment.yml

# install wheel
pip install {wheel}.whl
```
