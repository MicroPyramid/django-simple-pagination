from django.test import TestCase
from django.template import Template, Context
from django.http import HttpRequest
from simple_pagination.utils import(
    normalize_page_number,
    get_querystring_for_page,
    get_page_numbers,
)
from django.http import QueryDict


class PaginateAndShowPageItems(TestCase):

    def test_addition(self):
        t = Template(
            "{% load paginate %}{% paginate entities %}.{% show_pageitems %} {% paginate 20 entities %}")
        req = HttpRequest()
        c = Context({"entities": range(100), 'request': req})
        val = t.render(c)
        self.assertTrue(bool(val))


class NormalizePageNumber(TestCase):

    def test_normalize_page_number(self):
        page_number = 1
        page_range = range(2)
        val = normalize_page_number(page_number, page_range)
        self.assertTrue(bool(val))
        page_range = range(1)
        val = normalize_page_number(page_number, page_range)
        self.assertFalse(bool(val))


class GetQuerystringForPage(TestCase):

    def test_get_querystring_for_page(self):
        request = self
        request = HttpRequest()
        dict = {u"querystring_key": 1,
                u"key": 2,
                u"page": 3}
        qdict = QueryDict('', mutable=True)
        qdict.update(dict)
        request.GET = qdict
        val = get_querystring_for_page(request=request,
                                       page_number=1,
                                       querystring_key="key",
                                       default_number=1)
        self.assertTrue(bool(val))
        request.GET = {}
        val = get_querystring_for_page(request=request,
                                       page_number=1,
                                       querystring_key="key",
                                       default_number=1)
        self.assertFalse(bool(val))


class GetPageNumbers(TestCase):

    def test_get_page_numbers(self):
        get_page_numbers(current_page=2, num_pages=10)
        get_page_numbers(current_page=9, num_pages=10)
        get_page_numbers(current_page=1, num_pages=3)
