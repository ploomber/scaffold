# template


Minimal structure for bootstrapping Data Science projects

## Usage

```bash
# move to a folder where you want to store your project
mkdir my_new_project
cp my_new_project

# get template
curl -O -L https://github.com/ploomber/template/archive/master.zip

# unzip and run install script (will ask for a project name
# and a directory with that name will be created)
unzip master.zip
python template-master/install.py

# delete zip file
rm -f master.zip
```

## Testing

## Features

* `setup.py` following best practices, with commends for extensibility, install your pipeline using `pip install`
* Pre-configured testing suite, a simple test is provided to check that your package is installable via `pip install`
* Environment reproducibiliy is also tested using `nox`
* Sample `README.md` with instructions for development, testing and distribution
* Sample gitignore