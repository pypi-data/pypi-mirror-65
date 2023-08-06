# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starlette_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['prometheus_client>=0.7,<0.8', 'starlette>=0.12.2']

setup_kwargs = {
    'name': 'starlette-prometheus',
    'version': '0.6.0',
    'description': 'Prometheus integration for Starlette',
    'long_description': '# Starlette Prometheus\n[![Build Status](https://github.com/perdy/starlette-prometheus/workflows/Continuous%20Integration/badge.svg)](https://github.com/perdy/starlette-prometheus/actions)\n[![codecov](https://codecov.io/gh/perdy/starlette-prometheus/branch/master/graph/badge.svg)](https://codecov.io/gh/perdy/starlette-prometheus)\n[![Package Version](https://img.shields.io/pypi/v/starlette-prometheus?logo=PyPI&logoColor=white)](https://pypi.org/project/starlette-prometheus/)\n[![PyPI Version](https://img.shields.io/pypi/pyversions/starlette-prometheus?logo=Python&logoColor=white)](https://pypi.org/project/starlette-prometheus/)\n\n## Introduction\n\nPrometheus integration for Starlette.\n\n## Requirements\n\n* Python 3.6+\n* Starlette 0.9+\n\n## Installation\n\n```console\n$ pip install starlette-prometheus\n```\n\n## Usage\n\nA complete example that exposes prometheus metrics endpoint under `/metrics/` path.\n\n```python\nfrom starlette.applications import Starlette\nfrom starlette_prometheus import metrics, PrometheusMiddleware\n\napp = Starlette()\n\napp.add_middleware(PrometheusMiddleware)\napp.add_route("/metrics/", metrics)\n```\n\n## Contributing\n\nThis project is absolutely open to contributions so if you have a nice idea, create an issue to let the community \ndiscuss it.\n',
    'author': 'José Antonio Perdiguero López',
    'author_email': 'perdy@perdy.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PeRDy/starlette-prometheus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
