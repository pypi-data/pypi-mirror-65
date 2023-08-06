# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bronski', 'bronski.management', 'bronski.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['croniter>=0.3.31,<0.4.0', 'django>=2.2,<3.0']

setup_kwargs = {
    'name': 'bronski',
    'version': '0.3.3',
    'description': 'Simple, generic cron-like job runner service for Django',
    'long_description': '=======\nBronski\n=======\n\n.. rubric:: A beat server for Django, with cron-like syntax\n\nBronski allows you to configure periodic function calls using a Django model.\n\nIt is ideally suited to being a task "beat" sever, akin to celery-beat.\n\nInstall\n-------\n\n.. code-block:: sh\n\n    $ pip install bronski\n\n\nSetup\n-----\n\n1. Add \'bronski\' to your ``INSTALLED_APPS``\n\n   This is only needed to enable the management command.\n\n2. Create a model in your own app that inherits from ``bronski.models.CrontabBase``\n\n3. Create and apply migrations:\n\n   .. code-block:: sh\n\n    $ manage.py makemigrations\n    $ manage.py migrate\n\n4. Specify your model in settings\n\n   .. code-block:: python\n\n    CRONTAB_MODEL = "myapp.MyCronModel"\n\n5. Launch your beat server:\n\n   .. code-block:: sh\n\n    $ ./manage.py bronski\n\nEach minute the ``bronski`` service will scan the model for enabled jobs that\nhaven\'t been run in the past 59 seconds. It will then check each to see if its\ncrontab definition matches the next minute.\n\nFor job records that match, their ``run`` method will be called. The default\n``run`` method will:\n\n- get the specified function by calling ``self.get_function()``\n- resolve the ``kwargs`` to use by calling ``self.get_kwargs()``\n- invoke the function with the ``kwargs``.\n\nYou can override ``run`` in your custom model to, for instance, enqueue jobs:\n\n.. code-block:: python\n\n    class Jobs(CrontabBase):\n\n        def run(self):\n            func = self.get_function()\n            kwargs = self.get_kwargs()\n\n            # Celery task API:\n            func.delay(**kwargs)\n            # Dramatiq actor API:\n            func.send(**kwargs)\n',
    'author': 'Curtis Maloney',
    'author_email': 'curtis@tinbrain.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uptick/bronski',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
