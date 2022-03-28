from rest_framework import pagination


class NumberCursorPagination(pagination.CursorPagination):
    ordering = "number"
    page_size_query_param = "page_size"
    max_page_size = 200
