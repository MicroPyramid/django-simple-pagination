from django.conf import settings

PER_PAGE = getattr(settings, 'SIMPLE_PAGINATION_PER_PAGE', 10)
PAGE_LABEL = getattr(settings, 'SIMPLE_PAGINATION_PAGE_LABEL', 'page')
NEXT_LABEL = getattr(
    settings, 'SIMPLE_PAGINATION_NEXT_LABEL', '<span aria-hidden="true">&gt;</span>')
PREVIOUS_LABEL = getattr(
    settings, 'SIMPLE_PAGINATION_PREVIOUS_LABEL', '<span aria-hidden="true">&lt;</span>')
LAST_LABEL = getattr(
    settings, 'SIMPLE_PAGINATION_LAST_LABEL', '<span aria-hidden="true">&gt;&gt;</span>')
FIRST_LABEL = getattr(
    settings, 'SIMPLE_PAGINATION_FIRST_LABEL', '<span aria-hidden="true">&lt;&lt;</span>')
