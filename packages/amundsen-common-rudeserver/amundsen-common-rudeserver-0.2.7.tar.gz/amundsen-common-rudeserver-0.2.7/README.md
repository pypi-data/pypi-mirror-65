# Amundsen Common
[![PyPI version](https://badge.fury.io/py/amundsen-common.svg)](https://badge.fury.io/py/amundsen-common)
[![Build Status](https://api.travis-ci.org/lyft/amundsencommon.svg?branch=master)](https://travis-ci.org/lyft/amundsencommon)
[![Coverage Status](https://img.shields.io/codecov/c/github/lyft/amundsencommon/master.svg)](https://codecov.io/github/lyft/amundsencommon?branch=master)
[![License](http://img.shields.io/:license-Apache%202-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
[![Slack Status](https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social)](https://amundsenworkspace.slack.com/join/shared_invite/enQtNTk2ODQ1NDU1NDI0LTc3MzQyZmM0ZGFjNzg5MzY1MzJlZTg4YjQ4YTU0ZmMxYWU2MmVlMzhhY2MzMTc1MDg0MzRjNTA4MzRkMGE0Nzk)

Amundsen Common library holds common codes among micro services in Amundsen.
For information about Amundsen and our other services, visit the [main repository](https://github.com/lyft/amundsen). Please also see our instructions for a [quick start](https://github.com/lyft/amundsen/blob/master/docs/installation.md#bootstrap-a-default-version-of-amundsen-using-docker) setup  of Amundsen with dummy data, and an [overview of the architecture](https://github.com/lyft/amundsen/blob/master/docs/architecture.md).

## Requirements
- Python >= 3.6

## Buildint Pypi Distro

 1. Update version in setup.py
 2. Grab account credentials for PyPi [https://pypi.org/](https://pypi.org/)
 3. Build and upload distro:

```
# clean
deactivate
rm -rf venv/
rm -rf dist/

# venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 

# build / test
python3 setup.py install
python3 -bb -m pytest tests

# make dist
ls dist/
python3 setup.py sdist
ls dist/

# upload
pip install twine
twine upload dist/*
```

