# rescape-python-helpers
Functional and geospatial helpers

## Installation

Create a virtual environment using
```bash
mkdir ~/.virtualenvs
python3 -m venv ~/.virtualenvs/rescape-python-helpers
Activate it
source ~/.virtualenvs/rescape-python-helpers/bin/activate
```

#### Install requirements
```bash
$VIRTUAL_ENV/bin/pip install --no-cache-dir  --upgrade -r requirements.txt
```

Add the following to the bottom $VIRTUAL_ENV/bin/activate to setup the PYTHONPATH.
Replace the path with your code directory

```bash
export RESCAPE_PYTHON_HELPERS_BASE_DIR=/Users/andy/code/rescape-python-helpers
export RESCAPE_PYTHON_HELPERS_PROJECT_DIR=$RESCAPE_HELPERS_BASE_DIR/urbinsight
export PYTHONPATH=.:$RESCAPE_PYTHON_HELPERS_BASE_DIR:$RESCAPE_PYTHON_HELPERS_PROJECT_DIR
```

## Build

Update the version in setup.py
Run to generate build:
Update the version with bumpversion, which can't seem to look it up itself but udpates setup.py

```bash
git commit . -m "Version update" && git push
bumpversion --current-version {look in setup.py} patch setup.py
python3 setup.py clean sdist bdist_wheel
```

To distribute to testpypi site:
Upload package:

```bash
twine upload dist/*
```

To do everything at once

```bash
git commit . -m "Version update" && git push && bumpversion --current-version {look in setup.py} patch setup.py && python3 setup.py clean sdist bdist_wheel && twine upload dist/*
# Without the commit
bumpversion --current-version {look in setup.py} patch setup.py && python3 setup.py clean sdist bdist_wheel && twine upload dist/*
```

For setup of testpypi see ~/.pypirc or create one according to the testpypi docs:
e.g.:
[distutils]
index-servers=
    pypi
    testpypi

[testpypi]
repository: https://test.pypi.org/legacy/
username: your username for pypi.org
