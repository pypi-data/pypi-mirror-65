# [WIP] shtuka

<!--suppress HtmlDeprecatedAttribute -->
<div align="center">

[![Build Status](https://travis-ci.com/stasbel/shtuka.svg?token=1jgzjXXmtWmYE3GLcvgS&branch=master)](https://travis-ci.com/stasbel/shtuka)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

Neat and tidy configs gadget with methods on steroids 🔥

</div>

## installation

`pip install -e .`

## examples

### simple

```python
import shtuka
raw_config = {'optim': {'lr': 1e-3}}
config = shtuka.cook(raw_config)
assert raw_config['optim']['lr'] == 1e-3
assert config.optim.lr == 1e-3
```

### non strict

```python
import shtuka
raw_config = {'optim': {}}
config = shtuka.cook(raw_config, strict=False)
assert raw_config.get('optim', {}).get('lr', 5e-2) == 5e-2
assert config.optim.lr.or_(5e-2) == 5e-2
```

## tests

### local

```shell script
pip install -e '.[test]'
pytest
```

### tox

```shell script
pip install tox
tox
```

### CI

see [TravisCI config](.travis.yml)