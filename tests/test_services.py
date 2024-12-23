import pytest
from unittest.mock import MagicMock, ANY
from domain.entities import OrderItemEntity
from domain.exceptions import EntityNotFoundException
from domain.parameters import OrderFilters
from domain.services import OrderService


@pytest.fixture
def mock_order_repository():
    return MagicMock()


@pytest.fixture
def order_service(mock_order_repository):
    return OrderService(order_repository=mock_order_repository)


def test_register_order_success(order_service, mock_order_repository):
    mock_order_repository.get_last_order_sequence.return_value = MagicMock(
        last_order_id=123
    )
    mock_order_repository.save_order_sequence.return_value = None
    mock_order_repository.create.return_value = MagicMock(number="P000124")

    customer_id = 1
    items = [{"product_id": 101, "price": 10.0, "description": "Item 1", "quantity": 2}]
    total = 20.0

    order = order_service.register_order(
        customer_id=customer_id, items=items, total=total
    )

    assert order.number == "P000124"
    mock_order_repository.create.assert_called_once()


def test_find_all_order_success(order_service, mock_order_repository):
    mock_order_repository.list.return_value = [
        MagicMock(number="P000124"),
        MagicMock(number="P000125"),
    ]

    filters = OrderFilters(customer_id=1)

    orders = order_service.find_all_order(filters=filters)

    assert len(orders) == 2
    assert orders[0].number == "P000124"
    assert orders[1].number == "P000125"
    mock_order_repository.list.assert_called_once()


def test_find_all_order_not_found(order_service, mock_order_repository):
    mock_order_repository.list.return_value = []

    filters = OrderFilters(customer_id=1)

    with pytest.raises(EntityNotFoundException, match="No orders found."):
        order_service.find_all_order(filters=filters)

    mock_order_repository.list.assert_called_once()


def test_update_status_order_not_found(order_service, mock_order_repository):
    mock_order_repository.patch.return_value = None

    order_id = 1
    status = "RECEIVED"

    with pytest.raises(EntityNotFoundException, match="Order not found."):
        order_service.update_status_order(order_id=order_id, status=status)

    mock_order_repository.patch.assert_called_once()


def test_prepare_order_item(order_service):
    item_data = {
        "product_id": 101,
        "price": 10.0,
        "description": "Item 1",
        "quantity": 2,
    }

    item = order_service._prepare_order_item(item_data)

    assert isinstance(item, OrderItemEntity)
    assert item.product_id == 101
    assert item.price == 10.0
    assert item.description == "Item 1"
    assert item.quantity == 2
