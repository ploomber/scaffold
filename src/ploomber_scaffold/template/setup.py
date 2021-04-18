import versioneer

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

# NOTE: keep these lists updated as you add more dependencies to your project
# if you rather have any dependency installed via conda, add it here and in
# the environment.yml file

# minimum dependencies for deployment
REQUIRES = [
    'pyarrow',
    'numpy',
    'pandas',
    'ploomber',
    'scikit-learn',
]

# extra dependencies for development. e.g. run tests, build docs,
# train new models, generate exploratory notebooks, etc
REQUIRES_DEV = [
    'build',
    'pytest',
    'nox',
    'pyyaml',
    'invoke',
    'flake8',
    'jupyter',
    'matplotlib',
]

setup(
    name='package_name',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    # Include any non-Python files with these extensions, for details:
    # https://setuptools.readthedocs.io/en/latest/userguide/datafiles.html
    package_data={"": ["*/*.sql", "*/*.ipynb", "notebooks/*.py"]},
    install_requires=REQUIRES,
    extras_require={
        'dev': REQUIRES_DEV,
    },
)
