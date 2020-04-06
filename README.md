# template

[![Build Status](https://travis-ci.org/ploomber/template.svg?branch=master)](https://travis-ci.org/ploomber/template)

Minimal structure for bootstrapping Data Science projects

## Features

* `setup.py` following best practices, with commends for extensibility, install your pipeline using `pip install`
* Pre-configured testing suite, a simple test is provided to check that your package is installable via `pip install`
* Environment reproducibiliy is also tested using `nox`
* Sample `README.md` with instructions for development, testing and distribution
* Sample gitignore
* `setup.sh`
* `build.sh`

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
curl -O -L https://github.com/ploomber/template/archive/master.zip my_project/
cp my_new_project

unzip master.zip

# will prompt for the project's name
python template-master/install.py

# delete zip file
rm -f master.zip
```
