# CHANGELOG

## 0.2.2dev

* Adds `empty` option to create a `pipeline.yaml` with no tasks
* Fixes `fit.py `typo 

## 0.2.1 (2021-05-29)

* Customizes `README.md` content based on `conda` and `package` flags

## 0.2 (2021-05-22)

* Creates non-packaged pipeline by default
* Packaged pipeline available via the `--package` flag
* Generates `pip` `requirements.txt` files by default, `environment.yml` available via the `--conda` flag

## 0.1.3 (2021-04-18)

* Adds `python-versioneer` replacing our old implementation
* Moves `pipeline.yaml` to the new default location in `src/`
* Replaces example pipeline with one compatible with `OnlineModel`
* Updates `MANIFEST.in` to prevent temporary files to end up in the distribution file

## 0.1.2 (2021-03-07)

* A few information messages changed for clarity
* Adds a few comments to the sample pipeline for clarity
* Adds an example test that runs the pipeline and the example notebook
* Adds `CONTRIBUTING.md`
* `noxfile.py` checks for `environment.{lock}.yml` before starting
* Renames `invoke release` to `invoke version`

## 0.1.1 (2021-01-16)

* Removing some files that aren't needed for the template
* Works with Python 3.6


## 0.1

* First release
