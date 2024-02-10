# latin-macronizer

Script to automatically mark long vowels in Latin texts. Also optionally performs conversion of u to v and i to j.

Please see INSTALL.txt for installation instructions.

An official online version is currently located at http://www.alatius.com/macronizer/

## Development

Set up a virtualenv for the project. For example (using [pyenv] and [pyenv-virtualenv]):

```
$ pyenv virtualenv 3.12.0 macronizer
$ pyenv local macronizer
```

Install dependencies: `pip install -r requirements-dev.txt`

Install the package: `pip install -e .`

If you need to manage dependences, install [pip-tools]: `pip install pip-tools`

[pyenv]: https://github.com/pyenv/pyenv
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pip-tools]: https://github.com/jazzband/pip-tools
