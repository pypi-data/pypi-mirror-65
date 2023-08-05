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
    'version': '0.0.1',
    'description': 'A public read-only version of the Django Admin',
    'long_description': '# Django Public Admin\n\nA public and read-only version of the [Django Admin](https://docs.djangoproject.com/en/3.0/ref/contrib/admin/). A drop-in replacement for Django\'s native `AdminSite` and `ModelAdmin` for publicly accessible data.\n\n## How does it work\n\n1. `PublicAdminSite` works as a clone of Django\'s native `AdminSite`, but it looks at the HTTP request and the URL to decide whether they should exist in a public and read-only dashboard.\n1. `PublicModelAdmin` work as a clone of Django\'s native `ModelAdmin`, but what it does is to stop actions that would create, edit or delete objects.\n1. `DummyUser` is just a an implementation detail, since Django requires an user to process the requests.\n\n## Install\n\n> As this package is not finished nor published, this command does not work just yet. However, [Poetry](https://python-poetry.org/) should install it in the local _virtualenv_ one can access with `poetry shell`.\n\n```console\n$ pip install django-public-admin\n```\n\n## Usage\n\n### 1. Create your _Django Public Admin_ instance\n\nJust like one would create a regular `admin.py`, you can create a module using _Django Public Admin_\'s `PublicAdminSite` and `PublicModelAdmin`:\n\n```python\nfrom public_admin.admin import PublicModelAdmin\nfrom public_admin.sites import PublicAdminSite, PublicApp\n\nfrom my_website.my_open_house.models import Beverage, Snack\n\n\nclass BeverageModelAdmin(PublicModelAdmin):\n    pass\n\n\nclass SnackModelAdmin(PublicModelAdmin):\n    pass\n\n\npublic_app = PublicApp("my_open_house", models=("beverage", "snack"))\npublic_admin = PublicAdminSite(\n    "dashboard",  # you name it as you wish\n    public_app,  # this can be a single public app or a sequence of public apps\n)\npublic_admin.register(Beverage, BeverageModelAdmin)\npublic_admin.register(Sanck, SanckModelAdmin)\n```\n\n### 2. Add your _Django Public Admin_ URLs\n\nIn your `urls.py`, import the `public_html` (or whatever you\'ve named it earlier) in your URLs file and create the endpoints:\n\n```python\nfrom django.urls import path\n\nfrom my_website.my_open_house.admin import public_admin\n\n\nurl = [\n    # …\n    path("dashboard/", public_admin.urls)\n]\n```\n\n### 3. Templates\n\n_Django Public Admin_ comes with a template that hides from the UI elements related to user, login and logout. To use it, add `public_admin` to your `INSTALLED_APPS` **before** `django.contrib.admin`:\n\n```python\nINSTALLED_APPS = [\n    "public_admin",\n    "django.contrib.admin",\n    # ...\n]\n```\n\nIf you decide not to use it, you have to create your own `templates/base.html` to avoid errors when rendering the template. Django will fail, for example, in rendering URLs that do not exist, which would be the case for login and logout.\n\n## Contributing\n\nWe use `tox` to Run tests with Python 3.6, 3.7 and 3.8, and with Django 2 and 3. Also we use Black and `flake8`:\n\n```console\n$ poetry install\n$ poetry run tox\n```\n\n## License & Credits\n\nThis package is licensed under [MIT license](/LICENSE) and acknowledge [Serenata de Amor](https://github.com/okfn-brasil/serenata-de-amor) (© [Open Knowledge Brasil](https://br.okfn.org) and, previously, © [Data Science Brigade](https://github.com/datasciencebr)).\n',
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
