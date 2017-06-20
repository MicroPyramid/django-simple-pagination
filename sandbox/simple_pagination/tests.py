from django.test import TestCase
from django.template import Template, Context
from django.http import HttpRequest
from simple_pagination.utils import(
    normalize_page_number,
    get_querystring_for_page,
    get_page_numbers,
)
from simple_pagination.models import EndlessPage, PageList, ShowItems
from django.http import QueryDict
from django.core.paginator import Paginator


class PaginateAndShowPageItems(TestCase):

    def test_addition(self):
        t = Template(
            "{% load paginate %}{% paginate entities %}.{% show_pageitems %} {% paginate 20 entities %} {% show_pages %}")
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
        self.assertTrue(get_page_numbers(current_page=2, num_pages=10))
        self.assertTrue(get_page_numbers(current_page=9, num_pages=10))
        self.assertTrue(get_page_numbers(current_page=1, num_pages=3))


class TestEndlessPage(TestCase):

    def test_endless_page(self):
        request = HttpRequest()
        epage = EndlessPage(request=request,
                            number=2,
                            current_number=2,
                            total_number=10,
                            querystring_key='page')
        self.assertTrue(epage)


class TestPageList(TestCase):

    def test_page_list(self):
        request = HttpRequest()
        paginator = Paginator(['john', 'paul', 'george', 'ringo'], 3)
        page = paginator.page(1)
        page.number = lambda: None
        setattr(page, 'number', 2)
        setattr(page, 'paginator', paginator)
        page_list = PageList(request=request, page=page, querystring_key="page")
        page_list = PageList(request=request, page=page, querystring_key="page", default_number=1)
        page_list._endless_page(number=1)
        page_list._endless_page(number=3)
        self.assertTrue(page_list[1])
        page_list.next()
        self.assertTrue(page_list)
        si = ShowItems(request=request, page=page, querystring_key="page")
        self.assertTrue(si)
