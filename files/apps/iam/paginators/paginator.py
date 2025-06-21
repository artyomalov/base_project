from math import ceil
from pydantic import ValidationError


class Paginator:
    def __init__(self, limit: int, objects_count: int, current_page_num: int):
        if current_page_num < 1:
            raise ValidationError("Current_page_num must be more or equal 1")
        self._limit = limit
        self._objects_count = objects_count
        self._current_page_num = current_page_num

    @property
    def pages_count(self):
        pages_count = ceil(self._objects_count / self._limit)

        return pages_count

    @pages_count.setter
    def pages_count(self, value):
        raise Exception("Can't directly set value")

    @pages_count.deleter
    def pages_count(self):
        raise Exception("Can't delete value")

    @property
    def has_prev(self):
        return True if self._current_page_num > 1 else False

    @has_prev.setter
    def has_prev(self, value):
        raise Exception("Can't directly set value")

    @has_prev.deleter
    def has_prev(self):
        raise Exception("Can't directly delete value")

    @property
    def has_next(self):
        if self.pages_count != 0 and self._current_page_num > self.pages_count:
            raise ValidationError("Invalid page number")
        return True if self._current_page_num < self.pages_count else False

    @has_next.setter
    def has_next(self, value):
        raise Exception("Can't directly set value")

    @has_next.deleter
    def has_next(self):
        raise Exception("Can't directly delete value")
