from decimal import Decimal

from sqlalchemy import DECIMAL, String
from sqlmodel import cast, col, select
from sqlmodel.sql.expression import SelectOfScalar

from ..dependencies import SessionDep
from ..models.item_public import ItemPublic
from ..models.items_query_paginated import ItemsQueryPaginated
from ..params.filter_params_v2 import FilterParamsV2
from ..params.overall_params import OverallParams
from ..params.pagination_params import DEFAULT_LIMIT, DEFAULT_PAGE, PaginationParams
from ..params.sorting_params import SortingParams
from ..schemas.item import Item


class ItemsCrudV2:
    def create_item_query(self, overall_params: OverallParams):
        query: SelectOfScalar = select(Item)

        if overall_params.filters:
            query = self.create_filters_query(query, overall_params.filters)

        if overall_params.pagination:
            query = self.create_pagination_query(query, overall_params.pagination)

        if overall_params.sort:
            query = self.create_sorting_query(query, overall_params.sort)
        else:
            # Default query is sorted by category in ascending order then by name in ascending order
            query = self.create_default_sorted_query(query)

        return query

    def create_default_sorted_query(self, query: SelectOfScalar):
        return query.order_by(cast(Item.category, String).asc(), col(Item.name).asc())

    def create_filters_query(
        self, query: SelectOfScalar, filter_params: FilterParamsV2
    ) -> SelectOfScalar:
        if filter_params.dt_from:
            query = query.where(Item.last_updated_dt >= filter_params.dt_from)

        if filter_params.dt_to:
            query = query.where(Item.last_updated_dt <= filter_params.dt_to)

        if filter_params.category:
            query = query.where(Item.category == filter_params.category)

        if filter_params.name_contains:
            query = query.where(col(Item.name).contains(filter_params.name_contains))

        # Remember that Item.price is stored as a string
        if filter_params.price_range:
            min_price, max_price = filter_params.price_range
            query = query.where(
                cast(Item.price, DECIMAL(10, 2)).between(min_price, max_price)
            )

        return query

    def create_pagination_query(
        self, query: SelectOfScalar, pagination_params: PaginationParams
    ) -> SelectOfScalar:
        # All fields are already set
        page = pagination_params.page if pagination_params.page else DEFAULT_PAGE
        limit = pagination_params.limit if pagination_params.limit else DEFAULT_LIMIT
        return query.offset((page - 1) * limit).limit(limit)

    def create_sorting_query(
        self, query: SelectOfScalar, sorting_params: SortingParams
    ) -> SelectOfScalar:
        if not sorting_params.field and not sorting_params.order:
            return self.create_default_sorted_query(query)

        if sorting_params.field and hasattr(Item, sorting_params.field):
            column = col(getattr(Item, sorting_params.field))
            if sorting_params.order == "asc":
                query = query.order_by(column.asc())
            elif sorting_params.order == "desc":
                query = query.order_by(column.desc())

        return query

    def read_items_v2(
        self, session: SessionDep, overall_params: OverallParams
    ) -> ItemsQueryPaginated:
        query = self.create_item_query(overall_params)
        items_db = session.exec(query).all()

        items_public: list[ItemPublic] = []
        total_price: Decimal = Decimal(0)
        for item in items_db:
            item_public = ItemPublic.model_validate(item)
            items_public.append(item_public)
            total_price += item_public.price

        count = len(items_public)
        page = (
            overall_params.pagination.page
            # Check existence of these fields
            if (overall_params.pagination and overall_params.pagination.page)
            else DEFAULT_PAGE
        )
        limit = (
            overall_params.pagination.limit
            if (overall_params.pagination and overall_params.pagination.limit)
            else DEFAULT_LIMIT
        )

        return ItemsQueryPaginated(
            items=items_public,
            total_price=float(total_price),
            count=count,
            page=page,
            limit=limit,
        )


items_crud_v2 = ItemsCrudV2()
