# package_name

{%- if conda %}
Requires [Miniconda](https://docs.conda.io/en/latest/miniconda.html).
{%- endif %}

## Setup

```sh
# NOTE: if running ploomber <0.16, remove the --create-env argument
ploomber install --create-env

{%- if conda %}
# activate conda environment
conda activate package_name
{% else %}
# activate environment (unix)
source {path-to-venv}/bin/activate
# activate environment (windows cmd.exe)
{path-to-venv}\Scripts\activate.bat
# activate environment (windows PowerShell)
{path-to-venv}\Scripts\Activate.ps1
{%- endif %}
```

## Code editor integration

* If using Jupyter, [click here](https://docs.ploomber.io/en/latest/user-guide/jupyter.html)
* If using VSCode, PyCharm, or Spyder, [click here](https://docs.ploomber.io/en/latest/user-guide/editors.html)

{% if package %}
## Testing

```sh
pytest
```
{% endif %}

## Running the pipeline

```sh
ploomber build
```

## Help

* Need help? [Ask us anything on Slack!](https://ploomber.io/community)