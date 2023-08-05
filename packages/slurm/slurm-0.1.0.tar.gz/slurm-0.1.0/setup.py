# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slurm']

package_data = \
{'': ['*']}

install_requires = \
['simplejson', 'yaml']

setup_kwargs = {
    'name': 'slurm',
    'version': '0.1.0',
    'description': 'A bunch tools I have created over the years',
    'long_description': '![](pics/slurm.jpg)\n\n# Slurm\n\n**Under Development**\n\n\n```python\nfrom slurm import storage\n\nyaml = storage.read("file.yaml")\njson = storage.read("file.json")\njson = storage.read("file", "json")\n\n\ndata = [1,2,3,4]\nstorage.write("bob.json", data)\nstorage.write("guess", data, "yml")\n```\n',
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
