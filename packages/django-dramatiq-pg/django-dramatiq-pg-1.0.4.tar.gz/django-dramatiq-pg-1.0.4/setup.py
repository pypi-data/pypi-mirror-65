# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_dramatiq_pg', 'django_dramatiq_pg.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2', 'dramatiq-pg>=0.8.0']

setup_kwargs = {
    'name': 'django-dramatiq-pg',
    'version': '1.0.4',
    'description': 'Integration of Django with dramatiq-pg',
    'long_description': '==================\ndjango_dramatiq_pg\n==================\n\n.. rubric:: ``dramatiq-pg`` integration for django\n\nInstallation\n------------\n\n1. Install with pip\n\n   .. code-block:: sh\n\n    $ pip install django-dramatiq-pg\n\n2. Add to your ``INSTALLED_APPS`` list in settings.py\n\n   .. code-block:: python\n\n    INSTALLED_APPS = [\n        ...\n        \'django_dramatiq_pg\',\n    ]\n\n3. Configure the Database\n\n   .. code-block:: python\n\n    DRAMATIQ_BROKER = {\n        "OPTIONS": {\n            "url": "postgres:///mydb",\n        },\n        "MIDDLEWARE": [\n            "dramatiq.middleware.TimeLimit",\n            "dramatiq.middleware.Callbacks",\n            "dramatiq.middleware.Retries",\n        },\n    }\n\n4. Start the worker process:\n\n   .. code-block:: sh\n\n    $ dramatiq django_dramatiq_pg.worker\n\nThis worker module will auto-discover any module called \'actors\' in\n``INSTALLED_APPS``.\n\nSettings\n--------\n\nThis package attempts to retain backward compatibility with ``django-dramatiq``\nsettings, but ingores the `BROKER` key for `DRAMATIQ_BROKER`.\n\nSee https://github.com/Bogdanp/django_dramatiq for more details.\n\nDRAMATIQ_BROKER\n  A dict of options to pass when instantiating the broker.\n\nDRAMATIC_BROKER[\'OPTIONS\']\n  Arguments to pass to the Broker.\n\nDRAMATIC_BROKER[\'MIDDLEWARE\']\n  A list of middleware classes to be passed to the broker.\n\n  These can either be import strings, or instances.\n\nDRAMATIQ_ENCODER\n  Default: None\n\n  Import path for encoder class.\n\nDRAMATIQ_ACTORS_MODULE\n  Default: \'actors\'\n\n  Name of module use to auto-discover actors in INSTALLED_APPS.\n',
    'author': 'Curtis Maloney',
    'author_email': 'curtis@tinbrain.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uptick/django-dramatiq-pg',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
