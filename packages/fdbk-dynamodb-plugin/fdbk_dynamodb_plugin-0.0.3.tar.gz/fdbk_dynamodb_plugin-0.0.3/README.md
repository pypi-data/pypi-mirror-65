# fdbk_dynamodb_plugin

[![Build Status](https://travis-ci.org/kangasta/fdbk_dynamodb_plugin.svg?branch=master)](https://travis-ci.org/kangasta/fdbk_dynamodb_plugin)

AWS Dynamo DB wrapper for fdbk.

## Installation

Run:

```bash
pip install fdbk_dynamodb_plugin
```

to install from [PyPI](https://pypi.org/project/fdbk_dynamodb_plugin/) or download this repository and run

```bash
python setup.py install
```

to install from sources.

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle fdbk_dynamodb_plugin
autopep8 -aaar --in-place fdbk_dynamodb_plugin
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance fdbk_dynamodb_plugin
```

Run unit tests with command:

```bash
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```bash
coverage run --branch --source fdbk_dynamodb_plugin/ -m unittest discover -s tst/
coverage report -m
```
