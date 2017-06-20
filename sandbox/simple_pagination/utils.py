from __future__ import unicode_literals
import sys

from simple_pagination.settings import (
    PAGE_LABEL
)


# Handle the Python 2 to 3 migration.
if sys.version_info[0] >= 3:
    PYTHON3 = True
    text = str
else:
    PYTHON3 = False
    # Avoid lint errors under Python 3.
    text = unicode  # NOQA


def get_data_from_context(context):
    """Get the django paginator data object from the given *context*.
    The context is a dict-like object. If the context key ``endless``
    is not found, a *PaginationError* is raised.
    """
    try:
        return context['endless']
    except KeyError:
        raise Exception('Cannot find endless data in context.')


def get_page_number_from_request(
        request, querystring_key=PAGE_LABEL, default=1):
    """Retrieve the current page number from *GET* or *POST* data.
    If the page does not exists in *request*, or is not a number,
    then *default* number is returned.
    """
    try:
        return int(request.GET[querystring_key])
    except (KeyError, TypeError, ValueError):
        return default


def get_page_numbers(current_page, num_pages):
    """Default callable for page listing.
    Produce a Digg-style pagination.
    """

    if current_page <= 2:
        start_page = 1
    else:
        start_page = current_page - 2

    if num_pages <= 4:
        end_page = num_pages
    else:
        end_page = start_page + 4
        if end_page > num_pages:
            end_page = num_pages

    pages = []
    if current_page != 1:
        pages.append('first')
        pages.append('previous')
    pages.extend([i for i in range(start_page, end_page + 1)])
    if current_page != num_pages:
        pages.append('next')
        pages.append('last')
    return pages


def get_querystring_for_page(
        request, page_number, querystring_key, default_number=1):
    """Return a querystring pointing to *page_number*."""
    querydict = request.GET.copy()
    querydict[querystring_key] = page_number
    # For the default page number (usually 1) the querystring is not required.
    if page_number == default_number:
        del querydict[querystring_key]
    if 'querystring_key' in querydict:
        del querydict['querystring_key']
    if querydict:
        return '?' + querydict.urlencode()
    return ''


def normalize_page_number(page_number, page_range):
    """Handle a negative *page_number*.
    Return a positive page number contained in *page_range*.
    If the negative index is out of range, return the page number 1.
    """
    try:
        return page_range[page_number]
    except IndexError:
        return page_range[0]


class UnicodeMixin(object):
    """Mixin class to handle defining the proper unicode and string methods."""

    if PYTHON3:
        def __str__(self):
            return self.__unicode__()
