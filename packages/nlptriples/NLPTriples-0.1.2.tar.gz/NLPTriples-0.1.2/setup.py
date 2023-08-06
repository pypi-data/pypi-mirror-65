# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlptriples']

package_data = \
{'': ['*']}

install_requires = \
['benepar[cpu]>=0.1.2,<0.2.0',
 'cython>=0.29.16,<0.30.0',
 'numpy>=1.18.2,<2.0.0',
 'spacy>=2.2.4,<3.0.0',
 'tensorflow==1.15.2']

setup_kwargs = {
    'name': 'nlptriples',
    'version': '0.1.2',
    'description': 'A package to extract Triples in form of [predictate , object , subject]  form text ',
    'long_description': '# NLPTriples\nExtract NLP (RDF )Triples from a sentence\n',
    'author': 'adityaparkhi',
    'author_email': 'theaditya140@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
