# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'lib'}

modules = \
['flipt_pb2', 'flipt_pb2_grpc']
install_requires = \
['grpcio-tools>=1.28.1,<2.0.0',
 'grpcio>=1.28.1,<2.0.0',
 'protoc-gen-swagger>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'flipt-grpc-python',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'David Cramer',
    'author_email': 'dcramer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
