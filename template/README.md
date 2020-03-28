# package_name

TODO:
    1. Modify `environment.yml` with your supported Python version
    2. [add data files to gitignore] but let the user decide

## Develop

Once you cloned the repo:

```sh
pip install ".[dev]"
```

For running tests you also need: `pip install ".[test]"`

For building documentation: `pip install ".[doc]"`

## Testing

(`conda` is required)

```
nox
```

`nox` will create a temporary conda environment, if you want to run tests in the current Python environment:

```
pytest
```

## Distribution

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
