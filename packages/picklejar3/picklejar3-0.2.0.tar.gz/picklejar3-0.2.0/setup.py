# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['picklejar3']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'picklejar3',
    'version': '0.2.0',
    'description': 'A library to store data',
    'long_description': '# PickleJar3\n\n**Do not use, under development**\n\nSomething I wrote a while ago for storing data. I want to flush it out into\nsomething better.\n\n```python\n#!/usr/bin/env python3\nimport sys\nfrom picklejar3.picklejar import PickleJar\n\n\npj = PickleJar()\npj.init("bob.pickle", 3)\n\nfor i in range(9):\n    pj.push("a", i)\n\npj.push("b", 3.33)\npj.push("d", -1200)\n\npj.close()\n\npj.read("bob.pickle")\nprint(pj.buffer)\n```\n\n# MIT License\n\n**Copyright (c) 2020 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/picklejar3/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
