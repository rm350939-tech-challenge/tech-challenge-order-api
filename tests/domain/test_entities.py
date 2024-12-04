import pytest
from datetime import datetime
from domain.entities import (
    OrderStatus,
    OrderItemEntity,
    OrderEntity,
    OrderSequenceEntity,
)


def test_create_order_item_entity():
    item = OrderItemEntity(
        id=1,
        product_id=101,
        price=10.99,
        description="Test Product",
        quantity=2,
    )
    assert item.product_id == 101
    assert item.price == 10.99
    assert item.quantity == 2
    assert isinstance(item.created_at, datetime)


def test_order_item_from_dict():
    data = {
        "id": 1,
        "product_id": 101,
        "price": 10.99,
        "description": "Test Product",
        "quantity": 2,
        "created_at": datetime.now(),
    }
    item = OrderItemEntity.from_dict(data)
    assert item.product_id == 101
    assert item.description == "Test Product"


def test_create_order_entity():
    order = OrderEntity(
        id=1,
        number="12345",
        customer_id=501,
        items=[],
        total=0.0,
    )
    assert order.number == "12345"
    assert order.status == OrderStatus.PENDING
    assert order.total == 0.0


def test_add_item():
    order = OrderEntity(
        id=1,
        number="12345",
        customer_id=501,
        items=[],
        total=0.0,
    )
    order.add_item(product_id=101, quantity=2, price=20.9, description="Test Product")
    assert len(order.items) == 1
    assert order.items[0].product_id == 101


def test_order_as_dict():
    order = OrderEntity(
        id=1,
        number="12345",
        customer_id=501,
        items=[],
        total=0.0,
    )
    order_dict = order.as_dict()
    assert "number" in order_dict
    assert order_dict["number"] == "12345"


def test_order_from_dict():
    data = {
        "id": 1,
        "number": "12345",
        "customer_id": 501,
        "items": [
            {
                "id": 1,
                "product_id": 101,
                "price": 10.99,
                "description": "Test Product",
                "quantity": 2,
            }
        ],
        "total": 21.98,
        "status": 1,  # PENDING
    }
    order = OrderEntity.from_dict(data)
    assert order.number == "12345"
    assert order.status == OrderStatus.PENDING
    assert len(order.items) == 1


def test_create_order_sequence():
    sequence = OrderSequenceEntity(last_order_id=100)
    assert sequence.last_order_id == 100


def test_order_sequence_as_dict():
    sequence = OrderSequenceEntity(last_order_id=100)
    sequence_dict = sequence.as_dict()
    assert "last_order_id" in sequence_dict
    assert sequence_dict["last_order_id"] == 100


def test_order_sequence_from_dict():
    data = {"last_order_id": 100}
    sequence = OrderSequenceEntity.from_dict(data)
    assert sequence.last_order_id == 100
