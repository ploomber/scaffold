# Contributing

## Creating new stable versions

Before generating a new version, run tests and generate a lock file:

```sh
nox
```

Upon successful execution, edit your CHANGELOG file to add release notes.

Then create a new version using:


```sh
invoke version
```

And follow instructions.

**Note:** this will create (and push) a tag in your git repository.
