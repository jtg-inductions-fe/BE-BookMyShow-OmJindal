from rest_framework import pagination as rest_pagination


class MoviePagination(rest_pagination.CursorPagination):
    """
    Cursor-based pagination for the Movie list API.

    Attributes:
        page_size (int): Number of records returned per page (Default: 10).
        page_size_query_param (str): Client-side control for page size
        max_page_size (int): Maximum limit for the page_size parameter.
        ordering (str): The field used for cursor calculation.
    """

    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 50
    ordering = ("-release_date", "-id")
