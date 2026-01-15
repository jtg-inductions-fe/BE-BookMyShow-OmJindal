from rest_framework.pagination import CursorPagination


class MoviePagination(CursorPagination):
    """
    Pagination class for Movie list API.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    ordering = "-release_date"
