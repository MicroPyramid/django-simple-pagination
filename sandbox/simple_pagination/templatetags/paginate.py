"""Django Endless Pagination template tags."""

import re

from django import template
from simple_pagination import settings
from django.core.paginator import (
    EmptyPage,
    Paginator,
)
from simple_pagination import utils
from simple_pagination import models


PAGINATE_EXPRESSION = re.compile(r"""
    ^   # Beginning of line.
    (((?P<first_page>\w+)\,)?(?P<per_page>\w+)\s+)?  # First page, per page.
    (?P<objects>[\.\w]+)  # Objects / queryset.
    (\s+starting\s+from\s+page\s+(?P<number>[\-]?\d+|\w+))?  # Page start.
    (\s+using\s+(?P<key>[\"\'\-\w]+))?  # Querystring key.
    (\s+with\s+(?P<override_path>[\"\'\/\w]+))?  # Override path.
    (\s+as\s+(?P<var_name>\w+))?  # Context variable name.
    $   # End of line.
""", re.VERBOSE)
SHOW_CURRENT_NUMBER_EXPRESSION = re.compile(r"""
    ^   # Beginning of line.
    (starting\s+from\s+page\s+(?P<number>\w+))?\s*  # Page start.
    (using\s+(?P<key>[\"\'\-\w]+))?\s*  # Querystring key.
    (as\s+(?P<var_name>\w+))?  # Context variable name.
    $   # End of line.
""", re.VERBOSE)


register = template.Library()


@register.tag
def paginate(_, token, paginator_class=None):
    """Paginate objects.

    Usage:

    .. code-block:: html+django

        {% paginate entries %}

    After this call, the *entries* variable in the template context is replaced
    by only the entries of the current page.

    You can also keep your *entries* original variable (usually a queryset)
    and add to the context another name that refers to entries of the current
    page, e.g.:

    .. code-block:: html+django

        {% paginate entries as page_entries %}

    The *as* argument is also useful when a nested context variable is provided
    as queryset. In this case, and only in this case, the resulting variable
    name is mandatory, e.g.:

    .. code-block:: html+django

        {% paginate entries.all as entries %}

    The number of paginated entries is taken from settings, but you can
    override the default locally, e.g.:

    .. code-block:: html+django

        {% paginate 20 entries %}

    Of course you can mix it all:

    .. code-block:: html+django

        {% paginate 20 entries as paginated_entries %}

    By default, the first page is displayed the first time you load the page,
    but you can change this, e.g.:

    .. code-block:: html+django

        {% paginate entries starting from page 3 %}

    When changing the default page, it is also possible to reference the last
    page (or the second last page, and so on) by using negative indexes, e.g:

    .. code-block:: html+django

        {% paginate entries starting from page -1 %}

    This can be also achieved using a template variable that was passed to the
    context, e.g.:

    .. code-block:: html+django

        {% paginate entries starting from page page_number %}

    If the passed page number does not exist, the first page is displayed.

    If you have multiple paginations in the same page, you can change the
    querydict key for the single pagination, e.g.:

    .. code-block:: html+django

        {% paginate entries using article_page %}

    In this case *article_page* is intended to be a context variable, but you
    can hardcode the key using quotes, e.g.:

    .. code-block:: html+django

        {% paginate entries using 'articles_at_page' %}

    Again, you can mix it all (the order of arguments is important):

    .. code-block:: html+django

        {% paginate 20 entries
            starting from page 3 using page_key as paginated_entries %}

    Additionally you can pass a path to be used for the pagination:

    .. code-block:: html+django

        {% paginate 20 entries
            using page_key with pagination_url as paginated_entries %}

    This way you can easily create views acting as API endpoints, and point
    your Ajax calls to that API. In this case *pagination_url* is considered a
    context variable, but it is also possible to hardcode the URL, e.g.:

    .. code-block:: html+django

        {% paginate 20 entries with "/mypage/" %}

    If you want the first page to contain a different number of items than
    subsequent pages, you can separate the two values with a comma, e.g. if
    you want 3 items on the first page and 10 on other pages:

    .. code-block:: html+django

    {% paginate 3,10 entries %}

    You must use this tag before calling the {% show_more %} one.
    """
    # Validate arguments.
    try:
        tag_name, tag_args = token.contents.split(None, 1)
    except ValueError:
        msg = '%r tag requires arguments' % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)

    # Use a regexp to catch args.
    match = PAGINATE_EXPRESSION.match(tag_args)
    if match is None:
        msg = 'Invalid arguments for %r tag' % tag_name
        raise template.TemplateSyntaxError(msg)

    # Retrieve objects.
    kwargs = match.groupdict()
    objects = kwargs.pop('objects')

    # The variable name must be present if a nested context variable is passed.
    if '.' in objects and kwargs['var_name'] is None:
        msg = (
            '%(tag)r tag requires a variable name `as` argumnent if the '
            'queryset is provided as a nested context variable (%(objects)s). '
            'You must either pass a direct queryset (e.g. taking advantage '
            'of the `with` template tag) or provide a new variable name to '
            'store the resulting queryset (e.g. `%(tag)s %(objects)s as '
            'objects`).'
        ) % {'tag': tag_name, 'objects': objects}
        raise template.TemplateSyntaxError(msg)

    # Call the node.
    return PaginateNode(paginator_class, objects, **kwargs)


class PaginateNode(template.Node):
    """Add to context the objects of the current page.

    Also add the Django paginator's *page* object.
    """

    def __init__(self, paginator_class, objects, **kwargs):
        first_page = kwargs.get('first_page', None)
        per_page = kwargs.get('per_page', None)
        var_name = kwargs.get('var_name', None)
        number = kwargs.get('number', None)
        key = kwargs.get('key', None)
        override_path = kwargs.get('override_path', None)
        self.paginator = paginator_class or Paginator
        self.objects = template.Variable(objects)

        # If *var_name* is not passed, then the queryset name will be used.
        self.var_name = objects if var_name is None else var_name

        # If *per_page* is not passed then the default value from settings
        # will be used.
        self.per_page_variable = None
        if per_page is None:
            self.per_page = settings.PER_PAGE
        elif per_page.isdigit():
            self.per_page = int(per_page)
        else:
            self.per_page_variable = template.Variable(per_page)

        # Handle first page: if it is not passed then *per_page* is used.
        self.first_page_variable = None
        if first_page is None:
            self.first_page = None
        elif first_page.isdigit():
            self.first_page = int(first_page)
        else:
            self.first_page_variable = template.Variable(first_page)

        # Handle page number when it is not specified in querystring.
        self.page_number_variable = None
        if number is None:
            self.page_number = 1
        else:
            try:
                self.page_number = int(number)
            except ValueError:
                self.page_number_variable = template.Variable(number)

        # Set the querystring key attribute.
        self.querystring_key_variable = None
        if key is None:
            self.querystring_key = settings.PAGE_LABEL
        elif key[0] in ('"', "'") and key[-1] == key[0]:
            self.querystring_key = key[1:-1]
        else:
            self.querystring_key_variable = template.Variable(key)

        # Handle *override_path*.
        self.override_path_variable = None
        if override_path is None:
            self.override_path = None
        elif (
                override_path[0] in ('"', "'") and
                override_path[-1] == override_path[0]):
            self.override_path = override_path[1:-1]
        else:
            self.override_path_variable = template.Variable(override_path)

    def render(self, context):
        # Handle page number when it is not specified in querystring.
        if self.page_number_variable is None:
            default_number = self.page_number
        else:
            default_number = int(self.page_number_variable.resolve(context))

        # Calculate the number of items to show on each page.
        if self.per_page_variable is None:
            per_page = self.per_page
        else:
            per_page = int(self.per_page_variable.resolve(context))

        # User can override the querystring key to use in the template.
        # The default value is defined in the settings file.
        if self.querystring_key_variable is None:
            querystring_key = self.querystring_key
        else:
            querystring_key = self.querystring_key_variable.resolve(context)

        # Retrieve the override path if used.
        if self.override_path_variable is None:
            override_path = self.override_path
        else:
            override_path = self.override_path_variable.resolve(context)

        # Retrieve the queryset and create the paginator object.
        objects = self.objects.resolve(context)
        paginator = self.paginator(
            objects, per_page)

        # Normalize the default page number if a negative one is provided.
        if default_number < 0:
            default_number = utils.normalize_page_number(
                default_number, paginator.page_range)

        # The current request is used to get the requested page number.
        page_number = utils.get_page_number_from_request(
            context['request'], querystring_key, default=default_number)

        # Get the page.
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(1)

        # Populate the context with required data.
        data = {
            'default_number': default_number,
            'override_path': override_path,
            'page': page,
            'querystring_key': querystring_key,
        }
        context.update({'endless': data, self.var_name: page.object_list})
        return ''


@register.tag
def show_pages(_, token):
    """Show page links.

    Usage:

    .. code-block:: html+django

        {% show_pages %}

    It is just a shortcut for:

    .. code-block:: html+django

        {% get_pages %}
        {{ pages }}

    You can set ``ENDLESS_PAGINATION_PAGE_LIST_CALLABLE`` in your *settings.py*
    to a callable, or to a dotted path representing a callable, used to
    customize the pages that are displayed.

    See the *__unicode__* method of ``endless_pagination.models.PageList`` for
    a detailed explanation of how the callable can be used.

    Must be called after ``{% paginate objects %}``.
    """
    # Validate args.
    if len(token.contents.split()) != 1:
        msg = '%r tag takes no arguments' % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)
    # Call the node.
    return ShowPagesNode()


class ShowPagesNode(template.Node):
    """Show the pagination."""

    def render(self, context):
        # This template tag could raise a PaginationError: you have to call
        # *paginate* or *lazy_paginate* before including the getpages template.
        data = utils.get_data_from_context(context)
        # Return the string representation of the sequence of pages.
        pages = models.PageList(
            context['request'],
            data['page'],
            data['querystring_key'],
            default_number=data['default_number'],
            override_path=data['override_path'],
        )
        return utils.text(pages)


@register.tag
def show_pageitems(_, token):
    """Show page items.

    Usage:

    .. code-block:: html+django

        {% show_pageitems per_page %}

    """
    # Validate args.
    if len(token.contents.split()) != 1:
        msg = '%r tag takes no arguments' % token.contents.split()[0]
        raise template.TemplateSyntaxError(msg)
    # Call the node.
    return ShowPageItemsNode()


class ShowPageItemsNode(template.Node):
    """Show the pagination."""

    def render(self, context):
        # This template tag could raise a PaginationError: you have to call
        # *paginate* or *lazy_paginate* before including the getpages template.
        data = utils.get_data_from_context(context)
        pages = models.ShowItems(
            context['request'],
            data['page'],
            data['querystring_key'],
            default_number=data['default_number'],
            override_path=data['override_path'],
        )
        return utils.text(pages)
