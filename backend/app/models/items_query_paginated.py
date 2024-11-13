from ..models.items_query import ItemsQuery


class ItemsQueryPaginated(ItemsQuery):
    count: int
    page: int
    limit: int
