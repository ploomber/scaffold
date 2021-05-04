import versioneer

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

# deployment dependencies
REQUIRES = [
    'pandas',
    'ploomber',
    'scikit-learn',
    # uncomment the next line if you want to upload atifacts to S3...
    # 'boto3',
    # uncomment the next line if you want to upload atifacts to Google Cloud
    # Storage...
    # 'google-cloud-storage',
]

# development dependencies (e.g., testing, linting, etc)
REQUIRES_DEV = [
    'build',
    'pytest',
    'nox',
    'pyyaml',
    'invoke',
    'flake8',
    'jupyter',
    'matplotlib',
    # uncomment the next line if you want to export to systems like argo,
    # airflow or aws
    # 'soopervisor',
]

setup(
    name='package_name',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    install_requires=REQUIRES,
    extras_require={
        'dev': REQUIRES_DEV,
    },
)
