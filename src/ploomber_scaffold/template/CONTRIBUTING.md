# Contributing

## Creating new stable versions

Before generating a new version, run tests and generate a lock file:

```sh
nox
```

Upon successful execution, edit your CHANGELOG file to add release notes.

Then create a new version use [git tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging).