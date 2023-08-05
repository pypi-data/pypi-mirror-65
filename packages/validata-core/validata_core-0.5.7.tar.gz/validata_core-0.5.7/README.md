# Validata validation core

[![PyPI](https://img.shields.io/pypi/v/validata-core.svg)](https://pypi.python.org/pypi/validata-core)

Validata validation library built over Goodtables.

## Try

Create a virtualenv, run the script against fixtures:

```bash
mkvirtualenv validata
pip install -e .
validata --schema /path/to/schema.json table.csv
```

## Testing

```bash
pip install pytest
pytest --doctest-modules
```

## See also

- https://github.com/frictionlessdata/goodtables-py
- https://git.opendatafrance.net/validata/goodtables-checks-schema/
