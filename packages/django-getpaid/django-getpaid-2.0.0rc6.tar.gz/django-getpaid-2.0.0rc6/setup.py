# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getpaid', 'getpaid.backends', 'getpaid.backends.dummy', 'getpaid.migrations']

package_data = \
{'': ['*'], 'getpaid.backends.dummy': ['templates/getpaid_dummy_backend/*']}

install_requires = \
['django-model-utils>=4.0.0,<5.0.0',
 'pendulum>=2.0.5,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'sphinx-rtd-theme>=0.4.3,<0.5.0',
 'swapper>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'django-getpaid',
    'version': '2.0.0rc6',
    'description': 'Multi-broker payment processor for Django.',
    'long_description': '=============================\nWelcome to django-getpaid\n=============================\n\n.. image:: https://img.shields.io/pypi/v/django-getpaid.svg\n    :target: https://pypi.org/project/django-getpaid/\n    :alt: Latest PyPI version\n.. image:: https://img.shields.io/travis/sunscrapers/django-getpaid.svg\n    :target: https://travis-ci.org/sunscrapers/django-getpaid\n.. image:: https://img.shields.io/coveralls/github/cypreess/django-getpaid.svg\n    :target: https://coveralls.io/github/django-getpaid/django-getpaid?branch=master\n.. image:: https://img.shields.io/pypi/wheel/django-getpaid.svg\n    :target: https://pypi.org/project/django-getpaid/\n.. image:: https://img.shields.io/pypi/l/django-getpaid.svg\n    :target: https://pypi.org/project/django-getpaid/\n\n\ndjango-getpaid is a multi-broker payment processor for Django\n\nDocumentation\n=============\n\nThe full documentation is at https://django-getpaid.readthedocs.io.\n\nFeatures\n========\n\n* support for multiple payment brokers at the same time\n* clean but flexible architecture\n* support for asynchronous status updates - both push and pull\n* support for modern REST-based broker APIs\n* support for multiple currencies (but one per payment)\n* easy customization with provided base abstract models and swappable mechanic (same as with Django\'s User model)\n\n\nQuickstart\n==========\n\nInstall django-getpaid and at least one payment backend:\n\n.. code-block:: console\n\n    pip install django-getpaid\n    pip install django-getpaid-paynow\n\nAdd them to your ``INSTALLED_APPS``:\n\n.. code-block:: python\n\n    INSTALLED_APPS = [\n        ...\n        \'getpaid\',\n        \'getpaid_paynow\',  # one of plugins\n        ...\n    ]\n\nAdd getpaid to URL patterns:\n\n.. code-block:: python\n\n    urlpatterns = [\n        ...\n        path(\'payments/\', include(\'getpaid.urls\')),\n        ...\n    ]\n\nUse ``getpaid.models.AbstractOrder`` as parent class of your Order model and define minimal set of methods:\n\n.. code-block:: python\n\n    from getpaid.models import AbstractOrder\n\n    class MyCustomOrder(AbstractOrder):\n        amount = models.DecimalField(decimal_places=2, max_digits=8)\n        description = models.CharField(max_length=128)\n        buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)\n\n        def get_absolute_url(self):\n            return reverse(\'order-detail\', kwargs={"pk": self.pk})\n\n        def get_total_amount(self):\n            return self.amount\n\n        def get_user_info(self):\n            return {"email": self.buyer.email}\n\n        def get_description(self):\n            return self.description\n\n\nInform getpaid of your Order model in ``settings.py`` and provide settings for payment backends:\n\n.. code-block:: python\n\n    GETPAID_ORDER_MODEL = \'yourapp.MyCustomOrder\'\n\n    GETPAID_BACKEND_SETTINGS = {\n        \'getpaid_paynow\': {   # dotted import path of the plugin\n            # refer to backend docs for its real settings\n            "api_key": "9bcdead5-b194-4eb5-a1d5-c1654572e624",\n            "signature_key": "54d22fdb-2a8b-4711-a2e9-0e69a2a91189",\n        },\n    }\n\nAnd... provide some business logic ;)\n\nYour pre-payment view should use ``getpaid.forms.PaymentMethodForm`` `bound <https://docs.djangoproject.com/en/3.0/ref/forms/api/#ref-forms-api-bound-unbound>`_\nwith payment data. During binding the form will generate a list of plugins\n(payment methods) supporting your currency and hide rest of the fields.\nThen this form should be POSTed to ``{% url \'getpaid:create-payment\' %}`` to create\nnew payment. You should be automatically redirected to paywall. After payment\nyou should by default return to order-detail page but this behavior can be\nchanged by plugin\'s config.\n\nRunning Tests\n=============\n\nDoes the code actually work?\n\n.. code-block:: console\n\n    poetry install\n    poetry run tox\n\n\nCredits\n=======\n\nCreated by `Krzysztof Dorosz <https://github.com/cypreess>`_.\nRedesigned and rewritten by `Dominik Kozaczko <https://github.com/dekoza>`_.\n\nProudly sponsored by `SUNSCRAPERS <http://sunscrapers.com/>`_\n\nTools used in rendering this package:\n\n*  Cookiecutter_\n*  `cookiecutter-djangopackage`_\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage\n\n\nDisclaimer\n==========\n\nThis project has nothing in common with `getpaid <http://code.google.com/p/getpaid/>`_ plone project.\n',
    'author': 'Dominik Kozaczko',
    'author_email': 'dominik@kozaczko.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/django-getpaid/django-getpaid',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
