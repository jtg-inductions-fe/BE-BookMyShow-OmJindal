from rest_framework.pagination import PageNumberPagination


class CinemaPagination(PageNumberPagination):
    """
    Pagination class for Cinema list API.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
