Django-Simple-Pagination
=====

Django-Simple-Pagination is a simple Django app to for pagination.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Install 'Django-Simple-Pagination' using the following command.
    pip install django-simple-pagination

1. Add "simple_pagination" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'simple_pagination',
    ]
2. In templates use {% paginate entities %} to get pagination objects.
3. In templates use {% show_pages %} for getting the pages details.