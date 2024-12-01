import pytest
from domain.parameters import OrderFilters, OrderStatus


def test_order_filters_default_values():
    filters = OrderFilters()
    assert filters.customer_id is None
    assert filters.order == "asc"
    assert filters.sort == "created_at"
    assert filters.status == [
        OrderStatus.RECEIVED.name,
        OrderStatus.IN_PREPARATION.name,
        OrderStatus.READY.name,
    ]


def test_order_filters_custom_values():
    filters = OrderFilters(
        customer_id=123,
        order="desc",
        sort="updated_at",
        status=["PENDING", "COMPLETED"],
    )
    assert filters.customer_id == 123
    assert filters.order == "desc"
    assert filters.sort == "updated_at"
    assert filters.status == ["PENDING", "COMPLETED"]


def test_order_filters_partial_values():
    filters = OrderFilters(customer_id=456, order="desc")
    assert filters.customer_id == 456
    assert filters.order == "desc"
    assert filters.sort == "created_at"  # Default value
    assert filters.status == [
        OrderStatus.RECEIVED.name,
        OrderStatus.IN_PREPARATION.name,
        OrderStatus.READY.name,
    ]  # Default value
