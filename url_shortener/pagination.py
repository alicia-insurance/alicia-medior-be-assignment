from rest_framework.pagination import PageNumberPagination

"""
Custom pagination for scalable API.

Overrides default for easier future extension.
"""


class CustomShortURLPagination(PageNumberPagination):

    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100
