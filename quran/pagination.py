from rest_framework import pagination


class NumberCursorPagination(pagination.CursorPagination):
    ordering = "number"
