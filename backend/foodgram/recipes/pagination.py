from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class DefaultPagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    page_size_query_param = 'limit'
    max_page_size = 100
