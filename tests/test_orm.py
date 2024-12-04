from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest
from adapters.orm import OrderRepository
from domain.entities import (
    OrderEntity,
    OrderStatus,
)
from domain.parameters import OrderFilters


@pytest.fixture
def order_repository():
    return OrderRepository()


@patch("adapters.orm.OrderModel.create")
@patch("adapters.orm.OrderItemModel")
def test_create_order(mock_order_item_model, mock_order_model_create, order_repository):
    mock_order = MagicMock()
    mock_order_model_create.return_value = mock_order
    mock_order.model_to_dict.return_value = {
        "id": 1,
        "number": "P000001",
        "customer_id": 123,
        "status": OrderStatus.PENDING.value,
        "total": 100.0,
        "created_at": datetime(2023, 11, 30, 9, 0, 0),
        "updated_at": None,
        "items": [],
    }

    mock_order_item_model.return_value = MagicMock()

    order_entity = OrderEntity(
        id=None,
        number="P000001",
        customer_id=123,
        status=OrderStatus.PENDING,
        total=100.0,
        items=[],
        created_at=datetime(2023, 11, 30, 9, 0, 0),
        updated_at=None,
    )

    result = order_repository.create(order_entity=order_entity)

    mock_order_model_create.assert_called_once_with(
        number="P000001",
        customer_id=123,
        status=OrderStatus.PENDING.value,
        total=100.0,
        created_at=datetime(2023, 11, 30, 9, 0, 0),
    )
    assert result.number == "P000001"
    assert result.status == OrderStatus.PENDING


@patch("adapters.orm.OrderModel.select")
def test_list_orders(mock_order_model_select, order_repository):
    mock_order_query = MagicMock()
    mock_order = MagicMock()
    mock_order.model_to_dict.return_value = {
        "id": 1,
        "number": "P000001",
        "customer_id": 123,
        "status": OrderStatus.PENDING.value,
        "total": 100.0,
        "created_at": datetime(2023, 11, 30, 9, 0, 0),
        "updated_at": None,
        "items": [],
    }

    mock_order_query.where.return_value.order_by.return_value = [mock_order]
    mock_order_model_select.return_value = mock_order_query

    filters = OrderFilters(customer_id=123, status=["PENDING"], order="asc", sort="id")

    result = order_repository.list(filters=filters)

    mock_order_model_select.assert_called_once()
    mock_order_query.where.assert_called_once()
    mock_order_query.where.return_value.order_by.assert_called_once()
    assert len(result) == 1
    assert result[0].number == "P000001"
    assert result[0].status == OrderStatus.PENDING


@patch("adapters.orm.OrderModel.get_or_none")
def test_get_order_by_id(mock_get_or_none, order_repository):
    mock_order = MagicMock()
    mock_order.model_to_dict.return_value = {
        "id": 1,
        "number": "P000001",
        "customer_id": 123,
        "status": OrderStatus.PENDING.value,
        "total": 100.0,
        "created_at": datetime(2023, 11, 30, 9, 0, 0),
        "updated_at": None,
        "items": [],
    }
    mock_get_or_none.return_value = mock_order

    result = order_repository.get_by_id(order_id=1)

    mock_get_or_none.assert_called_once_with(id=1)
    assert result.number == "P000001"
    assert result.status == OrderStatus.PENDING


@patch("adapters.orm.OrderModel.get_or_none")
def test_patch_order(mock_get_or_none, order_repository):
    mock_order = MagicMock()
    mock_order.model_to_dict.return_value = {
        "id": 1,
        "number": "P000001",
        "customer_id": 123,
        "status": OrderStatus.READY.value,
        "total": 100.0,
        "created_at": datetime(2023, 11, 30, 9, 0, 0),
        "updated_at": datetime(2023, 11, 30, 12, 0, 0),
        "items": [],
    }
    mock_get_or_none.return_value = mock_order

    result = order_repository.patch(
        order_id=1,
        status=OrderStatus.READY,
        updated_at=datetime(2023, 11, 30, 12, 0, 0),
    )

    mock_get_or_none.assert_called_once_with(id=1)
    assert result.status == OrderStatus.READY


@patch("adapters.orm.OrderSequenceModel.select")
def test_get_last_order_sequence(mock_select, order_repository):
    mock_sequence = MagicMock()
    mock_sequence.model_to_dict.return_value = {"last_order_id": 10}
    mock_select.return_value.order_by.return_value.first.return_value = mock_sequence

    result = order_repository.get_last_order_sequence()

    assert result.last_order_id == 10


@patch("adapters.orm.OrderSequenceModel.create")
def test_save_order_sequence(mock_create, order_repository):
    mock_sequence = MagicMock()
    mock_sequence.model_to_dict.return_value = {"last_order_id": 11}
    mock_create.return_value = mock_sequence

    result = order_repository.save_order_sequence(last_order_id=11)

    mock_create.assert_called_once_with(last_order_id=11)
    assert result.last_order_id == 11
