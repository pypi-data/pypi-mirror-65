# flake8-import-order-tbm

[![PyPI](https://img.shields.io/pypi/v/flake8-import-order-tbm.svg?label=PyPI)](https://pypi.org/project/flake8-import-order-tbm/)
![](https://img.shields.io/badge/Python-3.6%2B-blue.svg)  
[![GitHub CI](https://img.shields.io/github/workflow/status/thebigmunch/flake8-import-order-tbm/CI?label=GitHub%20CI)](https://github.com/thebigmunch/flake8-import-order-tbm/actions?query=workflow%3ACI)  

[flake8-import-order-tbm](https://github.com/thebigmunch/flake8-import-order-tbm) is a style for
[flake8-import-order](https://github.com/PyCQA/flake8-import-order).


## Styling

* Package, module, and imported names are naturally sorted using [natsort](https://github.com/SethMMorton/natsort).
* Standard library import section precedes 3rd-party import section precedes local import section.
* Import statements precede from import statements.
* UPPERCASE precedes Capitalized precedes lowercase.
* Fewer levels in a local relative import precede greater levels.

A basic example:

```
import os
import sys
from os import path

import attr
import requests
from attr import attrib, attrs

import LocalPackage
import localpackage
from localpackage import name
from . import name1, name2, name10
from .module import name3
from ..module import name4
```

## Usage

Install ``flake8-import-order-tbm`` using ``pip install flake8-import-order-tbm``.

When running flake8, do one of the following:

* Add the ``--import-order-style=tbm`` option to the command.

* Add this to your [flake8 config](http://flake8.pycqa.org/en/latest/user/configuration.html):

	```
	import-order-style = tbm
	```
