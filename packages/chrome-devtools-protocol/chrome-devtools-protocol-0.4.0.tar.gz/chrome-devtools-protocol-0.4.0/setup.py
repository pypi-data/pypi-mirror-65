# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdp']

package_data = \
{'': ['*']}

install_requires = \
['deprecated>=1.2.9,<2.0.0']

setup_kwargs = {
    'name': 'chrome-devtools-protocol',
    'version': '0.4.0',
    'description': 'Python type wrappers for Chrome DevTools Protocol (CDP)',
    'long_description': '# PyCDP\n\n[![PyPI](https://img.shields.io/pypi/v/chrome-devtools-protocol.svg)](https://pypi.org/project/chrome-devtools-protocol/)\n![Python Versions](https://img.shields.io/pypi/pyversions/chrome-devtools-protocol)\n![MIT License](https://img.shields.io/github/license/HyperionGray/python-chrome-devtools-protocol.svg)\n[![Build Status](https://img.shields.io/travis/com/HyperionGray/python-chrome-devtools-protocol.svg?branch=master)](https://travis-ci.com/HyperionGray/python-chrome-devtools-protocol)\n[![Read the Docs](https://img.shields.io/readthedocs/py-cdp.svg)](https://py-cdp.readthedocs.io)\n\nPython Chrome DevTools Protocol (shortened to PyCDP) is a library that provides\nPython wrappers for the types, commands, and events specified in the [Chrome\nDevTools Protocol](https://github.com/ChromeDevTools/devtools-protocol/).\n\nThe Chrome DevTools Protocol provides for remote control of a web browser by\nsending JSON messages over a WebSocket. That JSON format is described by a\nmachine-readable specification. This specification is used to automatically\ngenerate the classes and methods found in this library.\n\nYou could write a CDP client by connecting a WebSocket and then sending JSON\nobjects, but this would be tedious and error-prone: the Python interpreter would\nnot catch any typos in your JSON objects, and you wouldn\'t get autocomplete for\nany parts of the JSON data structure. By providing a set of native Python\nwrappers, this project makes it easier and faster to write CDP client code.\n\n**This library does not perform any I/O!** In order to maximize\nflexibility, this library does not actually handle any network I/O, such as\nopening a socket or negotiating a WebSocket protocol. Instead, that\nresponsibility is left to higher-level libraries, for example\n[trio-chrome-devtools-protocol](https://github.com/hyperiongray/trio-chrome-devtools-protocol).\n\nFor more information, see the [complete documentation](https://py-cdp.readthedocs.io).\n\n<a href="https://www.hyperiongray.com/?pk_campaign=github&pk_kwd=pycdp"><img alt="define hyperion gray" width="500px" src="https://hyperiongray.s3.amazonaws.com/define-hg.svg"></a>\n',
    'author': 'Mark E. Haase',
    'author_email': 'mehaase@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hyperiongray/python-chrome-devtools-protocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
