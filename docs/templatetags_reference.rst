Templatetags reference
======================

.. _templatetags-paginate:

paginate
~~~~~~~~

Usage:

.. code-block:: html+django

    {% paginate items %}

After this call, the *items* variable in the template context is replaced
by only the entries of the current page.

You can also keep your *items* original variable (usually a queryset)
and add to the context another name that refers to items of the current page,
e.g.:

.. code-block:: html+django

    {% paginate items as page_items %}

The *as* argument is also useful when a nested context variable is provided
as queryset.

The number of paginated items is taken from SIMPLE_PAGINATION_PER_PAGE setting , but you can
override the default locally, e.g.:

.. code-block:: html+django

    {% paginate 20 items %}

Of course you can mix it all:

.. code-block:: html+django

    {% paginate 20 items as paginated_items %}

.. _templatetags-show_pageitems:

show_pageitems
~~~~~~~~~~~~~~

Show page items. Usage:

.. code-block:: html+django

    {% show_pageitems %}

The sequence can contain following values with other page links:

- *'previous'*: will display the previous page in that position;
- *'next'*: will display the next page in that position;
- *'first'*: will display the first page as an arrow;
- *'last'*: will display the last page as an arrow;

This must be called after `paginate`_.
