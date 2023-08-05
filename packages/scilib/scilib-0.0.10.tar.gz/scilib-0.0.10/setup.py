# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scilib',
 'scilib.db',
 'scilib.iolib',
 'scilib.scripts',
 'scilib.tests',
 'scilib.tests.test_wos',
 'scilib.wos']

package_data = \
{'': ['*'],
 'scilib.tests.test_wos': ['fixtures/*'],
 'scilib.wos': ['configs/*']}

install_requires = \
['jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.2,<2.0.0',
 'orjson>=2.6.3,<3.0.0',
 'pandas>=1.0.3,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'scipy>=1.4.1,<2.0.0',
 'xlrd>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'scilib',
    'version': '0.0.10',
    'description': 'scilib',
    'long_description': '\n# scilib\n\n[![Github](https://github.com/phyng/scilib/workflows/test/badge.svg)](https://github.com/phyng/scilib/actions) [![Pypi](https://img.shields.io/pypi/v/scilib.svg?style=flat&label=PyPI)](https://pypi.org/project/scilib/)\n\n## documentation\n\nhttps://phyng.com/scilib/\n\n## install\n\n```bash\n# use pip\npip install scilib\n\n# or use poetry\npoetry add scilib\n```\n\n## test\n\n```bash\nnpm test\nnpm test_coverage\n```\n\n## usage\n\n### import wos data to ElasticSearch\n\n```bash\nenv ES_API=http://localhost:9205 python -m scripts.import_to_es --from /path/to/wos_data/ --index wos\n```\n',
    'author': 'phyng',
    'author_email': 'phyngk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phyng/scilib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
