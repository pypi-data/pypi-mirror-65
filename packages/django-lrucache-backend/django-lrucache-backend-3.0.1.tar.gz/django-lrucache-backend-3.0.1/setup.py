# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lrucache_backend']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2', 'lru-dict>=1.1,<2.0']

setup_kwargs = {
    'name': 'django-lrucache-backend',
    'version': '3.0.1',
    'description': 'A smarter local memory cache backend for Django',
    'long_description': "django-lrucache-backend\n=======================\n\n.. image:: https://img.shields.io/pypi/v/django-lrucache-backend.svg\n    :target: https://pypi.python.org/pypi/django-lrucache-backend\n    :alt: Latest PyPI version\n\n.. image:: https://travis-ci.org/kogan/django-lrucache-backend.svg?branch=master\n   :target: https://travis-ci.org/kogan/django-lrucache-backend\n   :alt: Latest Travis CI build status\n\nA smarter local memory cache backend for Django.\n\n.. image:: benchmarking/2.0.0/objects-get.png\n   :alt: Cache Performance\n\n`Set Performance <benchmarking/2.0.0/objects-set.png>`_. `Delete performance\n<benchmarking/2.0.0/objects-delete.png>`_.\n\nAbout\n-----\n\n`lrucache_backend` is an in-memory cache that improves upon the existing\n`LocMemCache` that Django provides.\n\nComes with cache timeouts and a smart eviction strategy that prefers to keep\nkeys that are used often and evict keys that are not.\n\nOriginally developed to avoid poorly reimplementing local object stores for\nservice layer objects. For example:\n\n.. code-block:: python\n\n    def get_data_before(self):\n        if not hasattr(self, '__data'):\n            self.__data = self.expensive_query()\n        return self.__data\n\n    def get_data_after(self):\n        lcache = caches['local']\n        data = lcache.get('our_data')\n        if not data:\n            data = self.expensive_query()\n            lcache.set('our_data', data, timeout=600)\n        return data\n\nThe benefits (despite the longer method) include timeouts, sharing data between\nrequests, and avoiding network requests. This is especially useful when there\nare hundreds or thousands of property accesses that would hit the cache where\nnetwork overhead would be prohibitive. The `Fat model` pattern can greatly\nbenefit from tiered caching.\n\nGood for?\n^^^^^^^^^\n\nAn in memory cache is good for small data that changes rarely. It's effectively\na global dictionary shared between requests in the same process. Small lookup\ntables and database backed settings are good candidates.\n\nA small number of keys should be used to avoid engaging the culling strategy\nof the cache. Performance goes down fast as soon as the maximum number of keys\nare reached, and keys start to evict.\n\nThis should **not** be used as your primary cache, but it makes for an\nexcellent secondary cache when you want to avoid the overhead of a network call.\n\nUse for:\n\n- Small lookup tables\n- Settings\n- Backing store for your service objects\n- Remembering values for the duration of a request or celery task\n- Small global template fragments like sidebars or footers\n- Secondary cache\n\nBad for?\n^^^^^^^^\n\nAn in memory cache is terrible for data that changes often. Because the cache\nis process local, it's extremely difficult to coordinate cache invalidation\nfrom external processes. For that reason, this library does nothing to support\ncache invalidation.\n\nThe cache shares memory with the application, so it's extremely important to\navoid storing a lot of keys, or any large values.\n\nDo **not** use for:\n\n- Instance attributes/properties\n- Full templates\n- Tables with a large number of rows\n- Large values\n- Large lists\n- Primary cache\n\nDifferences from LocMemCache\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n- Avoids pickling\n- Avoids key name validation\n- Uses an LRU eviction algorithm rather than a random percentage culling strategy\n\nInstallation\n------------\n\n.. code-block:: bash\n\n     pip install django-lrucache-backend\n\nRequirements\n^^^^^^^^^^^^\n\n* `lru-dict <https://pypi.python.org/pypi/lru-dict/>`_.\n\n`lru-dict` is implemented in C and is unlikely to work with non-CPython\nimplementations. There *are* compatible pure python libraries. If you need this\nability, please open an Issue!\n\nUsage\n-----\n\nConfigure your `CACHES` Django setting appropriately:\n\n.. code-block:: python\n\n    CACHES = {\n        'local': {\n            'BACKEND': 'lrucache_backend.LRUObjectCache',\n            'TIMEOUT': 600,\n            'OPTIONS': {\n                'MAX_ENTRIES': 100\n            },\n            'NAME': 'optional-name'\n        }\n    }\n\nAnd then use the cache as you would any other:\n\n.. code-block:: python\n\n    >>> from django.core.cache import caches\n\n    >>> local = caches['local']\n    >>> local.set('key', 123)\n    >>> local.get('key')\n    ... 123\n\nIf you're going to use this cache backend, then it's highly recommended to use\nit as a non-default cache. That is, do not configure this cache under the\n`default` name.\n\nLocal memory caches compete for memory with your application so it's in your\nbest interests to use it as sparingly and deliberately as possible.\n\nCompatibility\n-------------\n\nDjango 2.2+\nPython 3.6+\n\nLicence\n-------\n\nMIT\n\nAuthors\n-------\n\n`django-lrucache-backend` was written by `Josh Smeaton <josh.smeaton@gmail.com>`_.\n",
    'author': 'Josh Smeaton',
    'author_email': 'josh.smeaton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kogan/django-lrucache-backend',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.4',
}


setup(**setup_kwargs)
