# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kungfupipelines']

package_data = \
{'': ['*']}

install_requires = \
['kfp>=0.1.36,<0.2.0', 'the-whole-caboodle>=0.2.10,<0.3.0']

setup_kwargs = {
    'name': 'kung-fu-pipelines',
    'version': '0.1.6',
    'description': 'Kubeflow pipelines made easy.',
    'long_description': None,
    'author': 'Saad Khan',
    'author_email': 'skhan8@mail.einstein.yu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
