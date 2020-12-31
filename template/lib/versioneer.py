"""
Managing project versions
"""
import sys
import ast
import re
import subprocess
import datetime
import os
from pathlib import Path


def replace_in_file(path_to_file, original, replacement):
    """Replace string in file
    """
    with open(path_to_file, 'r+') as f:
        content = f.read()
        updated = content.replace(original, replacement)
        f.seek(0)
        f.write(updated)
        f.truncate()


def read_file(path_to_file):
    with open(path_to_file, 'r') as f:
        content = f.read()

    return content


def call(*args, **kwargs):
    print(args, kwargs)
    # return subprocess.run(*args, **kwargs, check=True)


def input_str(prompt, default):
    response = input(prompt + f'. (Default: {default}): ')

    if not response:
        response = default

    return response


def input_confirm(prompt, default, abort):
    response_raw = input(prompt + '. Confirm? [y/n]: ')
    response = response_raw in {'y', 'Y', 'yes'}

    if not response and abort:
        print('Abort.')
        sys.exit(1)

    return response


class Versioner:
    """Utility functions to manage versions
    """
    def __init__(self, project_root='.'):
        self.path_to_src = Path(project_root, 'src')

        dirs = [
            f for f in os.listdir(self.path_to_src)
            if Path('src', f).is_dir() and not f.endswith('.egg-info')
        ]

        if len(dirs) != 1:
            raise ValueError(f'src/ must have a single folder, got: {dirs}')

        PACKAGE_NAME = dirs[0]
        self.PACKAGE = self.path_to_src / PACKAGE_NAME

    def current_version(self):
        """Returns the current version in __init__.py
        """
        _version_re = re.compile(r'__version__\s+=\s+(.*)')

        with open(self.PACKAGE / '__init__.py', 'rb') as f:
            VERSION = str(
                ast.literal_eval(
                    _version_re.search(f.read().decode('utf-8')).group(1)))

        return VERSION

    def release_version(self):
        """
        Returns a release version number
        e.g. 2.4.4dev -> v.2.2.4
        """
        current = self.current_version()

        if 'dev' not in current:
            raise ValueError('Current version is not a dev version')

        return current.replace('dev', '')

    def bump_up_version(self):
        """
        Gets gets a release version and returns a the next value value.
        e.g. 1.2.5 -> 1.2.6dev
        """
        # Get current version
        current = self.current_version()

        if 'dev' in current:
            raise ValueError('Current version is dev version, new dev '
                             'versions can only be made from release versions')

        # Get Z from X.Y.Z and sum 1
        tokens = current.split('.')

        # if just released a major version, add a 0 so we bump up a subversion
        # e.g. from 0.8 -> 0.8.0, then new dev version becomes 0.8.1dev
        if len(tokens) == 2:
            tokens.append('0')

        new_subversion = int(tokens[-1]) + 1

        # Replace new_subversion in current version
        tokens[-1] = str(new_subversion)
        new_version = '.'.join(tokens) + 'dev'

        return new_version

    def commit_version(self, new_version, tag=False):
        """
        Replaces version in  __init__ and optionally creates a tag in the git
        repository (also saves a commit)
        """
        current = self.current_version()

        # replace new version in __init__.py
        replace_in_file(self.PACKAGE / '__init__.py', current, new_version)

        # Create tag
        if tag:
            # Run git add and git status
            print('Adding new changes to the repository...')
            call(['git', 'add', '--all'])
            call(['git', 'status'])

            # Commit repo with updated dev version
            print('Creating new commit release version...')
            msg = 'Release {}'.format(new_version)
            call(['git', 'commit', '-m', msg])

            print('Creating tag {}...'.format(new_version))
            message = '{} release {}'.format(self.PACKAGE_NAME, new_version)
            call(['git', 'tag', '-a', new_version, '-m', message])

            print('Pushing tags...')
            call(['git', 'push', 'origin', new_version])

    def update_changelog_release(self, new_version):
        current = self.current_version()

        # update CHANGELOG header
        header_current = '{ver}\n'.format(ver=current) + '-' * len(current)
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        header_new = '{ver} ({today})\n'.format(ver=new_version, today=today)
        header_new = header_new + '-' * len(header_new)
        replace_in_file(self.path_to_src / 'CHANGELOG.rst', header_current,
                        header_new)

    def add_changelog_dev_section(self, dev_version):
        # add new CHANGELOG section
        start_current = 'Changelog\n========='
        start_new = (('Changelog\n=========\n\n{dev_version}\n'.format(
            dev_version=dev_version) + '-' * len(dev_version)) + '\n')
        replace_in_file(self.path_to_src / 'CHANGELOG.rst', start_current,
                        start_new)


def release(project_root='.', tag=True):
    """
    Create a new version for the project: updates __init__.py, CHANGELOG,
    creates new commit for released version (creating a tag) and commits
    to a new dev version
    """
    versioner = Versioner(project_root=project_root)

    current = versioner.current_version()
    release = versioner.release_version()

    release = input_str('Current version in app.yaml is {current}. Enter'
                        ' release version'.format(current=current),
                        default=release)

    versioner.update_changelog_release(release)

    changelog = read_file('CHANGELOG.rst')

    input_confirm('\nCHANGELOG.rst:\n\n{}\n Continue?'.format(changelog),
                  'done',
                  abort=True)

    # Replace version number and create tag
    print('Commiting release version: {}'.format(release))
    versioner.commit_version(release, tag=tag)

    # Create a new dev version and save it
    bumped_version = versioner.bump_up_version()

    print('Creating new section in CHANGELOG...')
    versioner.add_changelog_dev_section(bumped_version)
    print('Commiting dev version: {}'.format(bumped_version))
    versioner.commit_version(bumped_version)

    # Run git add and git status
    print('Adding new changes to the repository...')
    call(['git', 'add', '--all'])
    call(['git', 'status'])

    # Commit repo with updated dev version
    print('Creating new commit with new dev version...')
    msg = 'Bumps up project to version {}'.format(bumped_version)
    call(['git', 'commit', '-m', msg])
    call(['git', 'push'])

    print('Version {} was created, you are now in {}'.format(
        release, bumped_version))


def upload(tag, production):
    """
    Check outs a tag, uploads to PyPI
    """
    print('Checking out tag {}'.format(tag))
    call(['git', 'checkout', tag])

    current = Versioner.current_version()

    input_confirm('Version in {} tag is {}. Do you want to continue?'.format(
        tag, current))

    # create distribution
    call(['rm', '-rf', 'dist/'])
    call(['python', 'setup.py', 'sdist', 'bdist_wheel'])

    print('Publishing to PyPI...')

    if not production:
        call([
            'twine', 'upload', '--repository-url',
            'https://test.pypi.org/legacy/', 'dist/*'
        ])
    else:
        call(['twine', 'upload', 'dist/*'])