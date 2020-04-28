# Data Science template

[![Build Status](https://travis-ci.org/ploomber/template.svg?branch=master)](https://travis-ci.org/ploomber/template)

Template for Data Science projects.

Requires [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

## Features

* `setup.py` to easily set up your project as a Python package, no more messing around with `PYTHONPATH`. Install your project using `pip install`
* `setup.py` follows best practices and sets reasonable defaults, each section is clearly commented
* Pre-configured testing suite, a sample test is provided to check that your project imports correctly after installing it as a package using `pip install`
* Testing suite is triggered using `nox`, which will test your code in a clean conda environment, this ensures environment reproducibiliy. The environment is set up from the `environment.yml` file, a spec defined by conda itself
* Sample `README.md` with instructions for development, distribution and deployment
* `.gitignore` with defaults for Python and Jupyter notebooks
* `setup.sh` script for setting up the project from scratch: build conda environment and install project as a Python package
* `build.sh` script for generating a zip file that contains everything to deploy the project

## Usage

### Using it as a Github template

1) Click on the green "Use this template" button. [Or click here](https://github.com/ploomber/template/generate)

2) Follow the instructions for copying the template

3) Clone the repository with the template copy

```sh
git clone https://github.com/{username}/{repo_name}.git
cd {repo_name}/
```

4) Execute install script

```sh
# will prompt for the project's name
python install.py
```

5) Commit changes

```
git add --all
git commit -m 'Template applied'
```

### From the terminal

```bash
# get template
curl -O -L https://github.com/ploomber/template/archive/master.zip
unzip master.zip
rm master.zip

# will prompt for the project's name
cd template-master/
python install.py
```
