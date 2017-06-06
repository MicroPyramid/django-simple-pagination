.. image:: https://travis-ci.org/MicroPyramid/django-simple-pagination.svg?branch=master
   :target: https://travis-ci.org/MicroPyramid/django-simple-pagination

.. image:: https://img.shields.io/pypi/dm/django-simple-pagination.svg
    :target: https://pypi.python.org/pypi/django-simple-pagination
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/django-simple-pagination.svg
    :target: https://pypi.python.org/pypi/django-simple-pagination
    :alt: Latest Release

.. image:: https://coveralls.io/repos/github/MicroPyramid/django-simple-pagination/badge.svg?branch=master
   :target: https://coveralls.io/github/MicroPyramid/django-simple-pagination?branch=master

.. image:: https://landscape.io/github/MicroPyramid/django-simple-pagination/master/landscape.svg?style=flat
   :target: https://landscape.io/github/MicroPyramid/django-simple-pagination/master
   :alt: Code Health

.. image:: https://img.shields.io/github/license/micropyramid/django-simple-pagination.svg
    :target: https://pypi.python.org/pypi/django-simple-pagination/

`Django Simple Pagination`_ is a simple Django app to for digg-style pagination with little effort.

**Documentation** is `avaliable online`_, or in the docs
directory of the project.

Quick start
-----------

1. Install 'Django-Simple-Pagination' using the following command::

    pip install django-simple-pagination

2. Add ``simple_pagination`` to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'simple_pagination',
    ]
3. In templates use ``{% load paginate %}`` to load all pagination template tags
4. In templates use ``{% paginate no_of_records entities %}`` to get pagination objects.

    Here no_of_records means no of objects to display in a page and entities means the list of objects


5. In templates use ``{% show_pageitems %}`` to get digg-style page links.

Questions, Comments, etc?
-------------------------

We welcome your feedback and support, raise `github ticket`_ if you want to report a bug. Need new features? `Contact us here`_

Visit our Django web development page `Here`_

.. _contact us here: https://micropyramid.com/contact-us/
.. _avaliable online: http://django-simple-pagination.readthedocs.org/
.. _github ticket: https://github.com/MicroPyramid/django-simple-pagination/issues
.. _Django Simple Pagination: https://micropyramid.com/oss/
.. _Here: https://micropyramid.com/django-development-services/
