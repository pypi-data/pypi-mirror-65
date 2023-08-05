# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurm']

package_data = \
{'': ['*']}

install_requires = \
['colorama', 'pyyaml', 'simplejson']

setup_kwargs = {
    'name': 'slurm',
    'version': '0.2.0',
    'description': 'A bunch tools I have created over the years',
    'long_description': '![](pics/slurm.jpg)\n\n# Slurm\n\n\n[![Actions Status](https://github.com/MomsFriendlyRobotCompany/slurm/workflows/walchko%20pytest/badge.svg)](https://github.com/MomsFriendlyRobotCompany/slurm/actions)\n![GitHub](https://img.shields.io/github/license/MomsFriendlyRobotCompany/slurm)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/slurm)\n![PyPI](https://img.shields.io/pypi/v/slurm)\n\n**Under Development**\n\n\n```python\nfrom slurm import storage\n\nyaml = storage.read("file.yaml")\njson = storage.read("file.json")\njson = storage.read("file", "json")\n\n\ndata = [1,2,3,4]\nstorage.write("bob.json", data)\nstorage.write("guess", data, "yml")\n```\n\n# MIT License\n\n**Copyright (c) 2014 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/slurm/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
