# package_name

{%- if conda %}
Requires [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
{%- endif %}

## Setup development environment

```sh
# configure dev environment
ploomber install

{% if conda %}
# ...or use conda directly
conda env create --file environment.yml

# activate conda environment
conda activate package_name
{% else %}
# ...or use venv directly (choose a path-to-venv)
python -m venv {path-to-venv}

# activate environment (unix)
source {path-to-venv}/bin/activate
# activate environment (windows cmd.exe)
{path-to-venv}\Scripts\activate.bat
# activate environment (windows PowerShell)
{path-to-venv}\Scripts\Activate.ps1

# the install dependencies
pip install --requirement requirements.txt
{% endif %}

{%- if package %}
# after activating your environment, install your project with
pip install --editable .
# note: you can skip this step if using "ploomber install"
{% endif -%}
```

{% if package %}
## Testing

```sh
pytest
```
{% endif %}

## Running the pipeline

```sh
ploomber build

# start an interactive session
ploomber interact
```

## Exporting to other systems

[soopervisor](https://soopervisor.readthedocs.io/) allows you to run ploomber projects in other environments (Kubernetes, AWS Batch, AWS Lambda and Airflow). Check out the docs to learn more.
