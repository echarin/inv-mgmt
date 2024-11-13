from enum import Enum


class Category(str, Enum):
    stationery = "stationery"
    electronics = "electronics"
    books = "books"
    clothing = "clothing"
    furniture = "furniture"

    @classmethod
    def values(cls):
        return [e.value for e in cls]