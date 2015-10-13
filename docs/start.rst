Getting started
===============

Requirements
~~~~~~~~~~~~

======  ====================
Python  >= 2.6 (or Python 3)
Django  >= 1.3
jQuery  >= 1.7
======  ====================

Installation
~~~~~~~~~~~~

The Git repository can be cloned with this command::

    git clone https://github.com/MicroPyramid/django-simple-pagination.git

The ``simple_pagination`` package, included in the distribution, should be
placed on the ``PYTHONPATH``.

Otherwise you can just ``easy_install -Z django-simple-pagination``
or ``pip install django-simple-pagination``.

Settings
~~~~~~~~

Add the request context processor to your *settings.py*, e.g.::

    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    TEMPLATE_CONTEXT_PROCESSORS += (
        'django.core.context_processors.request',
    )

Add ``'simple_pagination'`` to the ``INSTALLED_APPS`` to your *settings.py*.

See the :doc:`settings` section for other settings.

Quickstart
~~~~~~~~~~

Given a template like this:

.. code-block:: html+django

    {% for item in items %}
        {# your code to show the item #}
    {% endfor %}

you can use simple Digg-style pagination to display objects just by adding:

.. code-block:: html+django

    {% load paginate %}

    {% paginate items %}
    {% for item in items %}
        {# your code to show the item #}
    {% endfor %}
    {% show_pageitems %}

Done.

This is just a basic example. To continue exploring all the Django Simple
Pagination features, have a look at :doc:`simple_pagination`.