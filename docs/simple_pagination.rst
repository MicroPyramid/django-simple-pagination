Simple pagination
=====================

Simple pagination is nothing but a basic Digg-style pagination of queryset objects. It is really easy to implement. All you have to do is modifying the template, e.g.:

.. code-block:: html+django

    {% load paginate %}

    {% paginate items %}
    {% for item in items %}
        {# your code to show the item #}
    {% endfor %}
    {% show_pageitems %}

That's it! As seen, the :ref:`templatetags-paginate` template tag takes care of
customizing the given queryset and the current template context. The
:ref:`templatetags-show_pageitems` one displays the page links allowing for
navigation to other pages including previous, next, first and last links.