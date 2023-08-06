# lhub_integ
Python package to shim basic scripts to work with integration machinery.
This package requires Python 3.6:
```
# Optional: install Python 3.6 with pyenvv
brew install pyenv
pyenv install 3.6.6
pyenv init # Follow the instructions
pyenv local 3.6.6
python --version
```

```
pip install lhub_integ
```

## Usage (as an integration writer)
To write a Python script that is convertible into an integration:

1. Create a directory that will contain your integration
2. Install lhub_integ as a local package:
```pip install lhub_integ```

Python scripts must provide an entrypoint function with some number of arguments. These arguments will correspond to columns
in the input data. The function should return a Python dictionary that can be serialized to JSON

```python
def process(url, num_bytes: int):
  return {'output': url + 'hello'}
```

### Specifying Dependencies
You must create a `requirements.txt` file specifying your dependencies. To create a dependency bundle run:
```
$ bundle-requirements
```
This script is provided when you install lhub_integ.

### Publishing
You will need the PyPi username and password that are in 1Password (search for PyPi)

1. Bump the version in pyproject.toml

2. `poetry publish --build`
