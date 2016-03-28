Django-Simple-Pagination
=========================

.. image:: https://travis-ci.org/MicroPyramid/django-simple-pagination.svg?branch=master
   :target: https://travis-ci.org/MicroPyramid/django-simple-pagination

.. image:: https://coveralls.io/repos/github/MicroPyramid/django-simple-pagination/badge.svg?branch=master
   :target: https://coveralls.io/github/MicroPyramid/django-simple-pagination?branch=master

.. image:: https://landscape.io/github/MicroPyramid/django-simple-pagination/master/landscape.svg?style=flat
   :target: https://landscape.io/github/MicroPyramid/django-simple-pagination/master
   :alt: Code Health

Django-Simple-Pagination is a simple Django app to for digg-style pagination with little effort.

**Documentation** is `avaliable online
<http://django-simple-pagination.readthedocs.org/>`_, or in the docs
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
2. In templates use ``{% paginate entities %}`` to get pagination objects.
3. In templates use ``{% show_pageitems %}`` to get digg-style page links.
