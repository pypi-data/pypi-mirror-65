# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eigpca']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0', 'numpy>=1.18.2,<2.0.0']

setup_kwargs = {
    'name': 'eigpca',
    'version': '0.1.0',
    'description': 'Principal Component Analysis via eigen-decomposition of the covariance/correlation matrix',
    'long_description': '# eigpca\nPCA via eigen-decomposition of the covariance/correlation matrix.\n\n# Install\n```bash\npip install eigpca\n```\n\n# Example\n```python\nfrom eigpca import PCA\nfrom sklearn.datasets import load_iris\n\nX = load_iris().data\npca = PCA()\n\npca.fit(X)\npca.transform(X, n_components=2)\n```\n### Scree Plot\n```python\npca.plot(y="pov")\n```\n![Scree plot](examples/scree_plot_iris.png)\n\n',
    'author': 'Sercan Dogan',
    'author_email': 'sercandogan@yandex.com',
    'maintainer': 'Sercan Dogan',
    'maintainer_email': 'sercandogan@yandex.com',
    'url': 'https://github.com/sercandogan/eigpca/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
