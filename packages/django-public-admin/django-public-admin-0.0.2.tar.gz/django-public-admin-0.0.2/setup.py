# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['public_admin']

package_data = \
{'': ['*'], 'public_admin': ['templates/admin/*']}

install_requires = \
['django>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'django-public-admin',
    'version': '0.0.2',
    'description': 'A public read-only version of the Django Admin',
    'long_description': "[![PyPI](https://img.shields.io/pypi/v/django-public-admin)](https://pypi.org/project/django-public-admin/) [![Documentation Status](https://readthedocs.org/projects/django-public-admin/badge/?version=latest)](https://django-public-admin.readthedocs.io/en/latest/?badge=latest) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-public-admin)](https://pypi.org/project/django-public-admin/) [![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-public-admin)](https://pypi.org/project/django-public-admin/)\n\n# Django Public Admin\n\n\nA public and read-only version of the [Django Admin](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/). A drop-in replacement for Django's native `AdminSite` and `ModelAdmin` for publicly accessible data. Check the [documentation](https://django-public-admin.readthedocs.io/en/latest/?badge=latest) for more information on how to use it.\n\n## Contributing\n\nWe use `tox` to Run tests with Python 3.6, 3.7 and 3.8, and with Django 2 and 3. Also we use Black and `flake8`:\n\n```console\n$ poetry install\n$ poetry run tox\n```\n\n### Docs\n\nTo build the docs we use [Sphinx](https://www.sphinx-doc.org/en/):\n\n```\n$ poetry run sphinx-build docs docs/_build/\n```\n\nThem just jump to `docs/_build/index.html`.\n\n## License & Credits\n\nThis package is licensed under [MIT license](/LICENSE) and acknowledge [Serenata de Amor](https://github.com/okfn-brasil/serenata-de-amor) (© [Open Knowledge Brasil](https://br.okfn.org) and, previously, © [Data Science Brigade](https://github.com/datasciencebr)).\n",
    'author': 'Eduardo Cuducos',
    'author_email': 'cuducos@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cuducos/django-public-admin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
