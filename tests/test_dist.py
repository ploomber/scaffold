"""
Check that source and wheel distribution files contain the right set of files

This covers two scenarios"

Extra files. Some tmp files are generated while developing the project (e.g,
products when calling "ploomber build" in the sample pipeline).

Missing files. By default, a Python package does not include non .py files,
to allow them, we have to indicate so in the MANIFEST.in file, but it's easy
to forget that when adding files.

In both scenarios, we rely compare the contents of the generated
with the files tracked by git.
"""
from itertools import chain
from glob import iglob
import os
import subprocess
from pathlib import Path
import shutil
import zipfile
import tarfile

import pytest


def git_tracked_files():
    out = subprocess.check_output(
        ['git', 'ls-tree', '-r', 'HEAD', '--name-only'])
    return out.decode().splitlines()


def glob_all(path):
    hidden = iglob(str(path / '**' / '.*'), recursive=True)
    normal = iglob(str(path / '**'), recursive=True)
    return chain(hidden, normal)


def files_in_directory(path, exclude_pyc=True):
    path = Path(path)
    files = [
        str(Path(f).relative_to(path)) for f in glob_all(path)
        if '__pycache__' not in f and Path(f).is_file()
    ]

    if exclude_pyc:
        files = [f for f in files if '.pyc' not in f]

    return files


def extract_zip(path, tmp_path):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(tmp_path)


def extract_tar(path, tmp_path):
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(tmp_path)


def get_dist_dir_name(tmp_path):
    if any('.dist-info' in f for f in os.listdir(tmp_path)):
        # wheel
        return Path(tmp_path, 'package_name')
    else:
        # source dist
        dir_name = os.listdir(tmp_path)[0]
        return Path(tmp_path, dir_name, 'src', 'package_name')


def assert_same_files(reference, directory):
    expected = set(reference)
    existing = set(directory)

    missing = expected - existing
    extra = existing - expected

    if missing:
        raise ValueError(f'missing files: {missing}')

    if extra:
        raise ValueError(f'extra files: {extra}')


@pytest.fixture
def move_to_template():
    old = os.getcwd()

    os.chdir(Path('src', 'ploomber_scaffold', 'template'))

    yield

    os.chdir(old)


@pytest.mark.parametrize('fmt, extractor', [
    ['bdist_wheel', extract_zip],
    ['sdist', extract_tar],
],
                         ids=['wheel', 'sdist'])
def test_template_dist_contains_all_files(fmt, extractor, tmp_path,
                                          move_to_template):
    if Path('build').exists():
        shutil.rmtree('build')

    if Path('dist').exists():
        shutil.rmtree('dist')

    if Path('src', 'package_name.egg-info').exists():
        shutil.rmtree(Path('src', 'package_name.egg-info'))

    subprocess.run(['python', 'setup.py', fmt], check=True)
    extractor(Path('dist', os.listdir('dist')[0]), tmp_path)

    path_dist = get_dist_dir_name(tmp_path)

    reference = [
        str(Path(f).relative_to('src/package_name'))
        for f in git_tracked_files() if 'package_name' in f
    ]

    generated = files_in_directory(path_dist, exclude_pyc=False)

    assert reference
    assert generated
    assert_same_files(reference, generated)


# TODO: test common actions: add another yaml, py, ipynb, sql, md, etc. and
# make sure the files are included in wheels and sdist
