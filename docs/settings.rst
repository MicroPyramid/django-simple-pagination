********
Settings
********

.. highlight:: python

``SIMPLE_PAGINATION_PER_PAGE``
==============================

- Default: ``10``

This tells the pagiante tag how many objects are normally displayed in a page (overwriteable by templatetag).


``ENDLESS_PAGINATION_PAGE_LABEL``
=================================

- Default: ``'page'``

This is the the querystring key of the page number (e.g. http://example.com?page=2).


``SIMPLE_PAGINATION_NEXT_LABEL``
================================

- Default: ``'<span aria-hidden="true">&gt;</span>'``

This is the default label for the previous page link.


``SIMPLE_PAGINATION_PREVIOUS_LABEL``
=====================================

- Default ``'<span aria-hidden="true">&lt;</span>'``

This is the default label for the next page link.


``SIMPLE_PAGINATION_LAST_LABEL``
=================================

- Default: ``'<span aria-hidden="true">&gt;&gt;</span>'``

This is the default label for the last page link.

``SIMPLE_PAGINATION_FIRST_LABEL``
=================================

- Default: ``'<span aria-hidden="true">&lt;&lt;</span>'``

This is the default label for the first page link.
