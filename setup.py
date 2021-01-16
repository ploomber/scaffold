import io
import re
import ast
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/ploomber_scaffold/__init__.py', 'rb') as f:
    VERSION = str(
        ast.literal_eval(
            _version_re.search(f.read().decode('utf-8')).group(1)))


def read(*names, **kwargs):
    return io.open(join(dirname(__file__), *names),
                   encoding=kwargs.get('encoding', 'utf8')).read()


DEV = [
    'twine',
    'flake8',
    'yapf',
    'pytest',
    'invoke',
    'ipython',
    'nox',
    # ipython not yet compatible with the latest version of jedi
    'jedi==0.17.2',
    # to make this work in Python < 3.7
    'importlib_resources;python_version<"3.7"',
]

setup(
    name='ploomber-scaffold',
    version=VERSION,
    description=None,
    long_description=None,
    author=None,
    author_email=None,
    url='https://github.com/ploomber/ploomber-scaffold',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[],
    extras_require={
        'dev': DEV,
    },
)
