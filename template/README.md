# package_name

TODO:
1. Modify `environment.yml` with your supported Python version
2. Review dependencies to install via conda
3. Install conda environment `conda env create -f environment.yml`
4. Activate environment `conda activate package_name`
5. Install your package in editable mode, with all depdencies inside the conda environment `pip install --editable ".[all]"`
6. [add data files to gitignore] but let the user decide

## Setup development environment

Once you cloned the repo, run `bash setup.sh`, requires conda.

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
bash distribute/main/build.sh

# zips environment.yml, wheel and setup.sh
```



## Deployment


Although the usual `pip install {wheel}.whl` is supported, this project has non-Python dependencies that are better handled via `conda`, the recommended installation procedure is as follows:

```
unzip dist-main.zip
cd dist-main/
bash setup.sh
```

Use the process manager of your choice


