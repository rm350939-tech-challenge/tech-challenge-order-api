from datetime import datetime
from domain.entities import OrderEntity, OrderItemEntity, OrderStatus
from adapters.dto import OrderItemDTO, OutputOrderDTO


def test_order_item_dto_from_domain():
    item_entity = OrderItemEntity(
        id=1,
        product_id=101,
        description="Test Product",
        price=50.0,
        quantity=2,
        created_at=datetime(2023, 11, 30, 10, 0, 0),
        updated_at=datetime(2023, 11, 30, 12, 0, 0),
    )

    item_dto = OrderItemDTO.from_domain(item_entity)

    assert item_dto.id == 1
    assert item_dto.product_id == 101
    assert item_dto.description == "Test Product"
    assert item_dto.price == 50.0
    assert item_dto.quantity == 2


def test_output_order_dto_from_domain():
    item_entity = OrderItemEntity(
        id=1,
        product_id=101,
        description="Test Product",
        price=50.0,
        quantity=2,
        created_at=datetime(2023, 11, 30, 10, 0, 0),
        updated_at=datetime(2023, 11, 30, 12, 0, 0),
    )

    order_entity = OrderEntity(
        id=1,
        number="P000001",
        customer_id=123,
        status=OrderStatus.PENDING,
        total=100.0,
        items=[item_entity],
        created_at=datetime(2023, 11, 30, 9, 0, 0),
        updated_at=datetime(2023, 11, 30, 12, 0, 0),
    )

    order_dto = OutputOrderDTO.from_domain(order_entity)

    assert order_dto.id == 1
    assert order_dto.number == "P000001"
    assert order_dto.customer_id == 123
    assert order_dto.status == "PENDING"
    assert order_dto.total == 100.0
    assert len(order_dto.items) == 1
    assert order_dto.items[0].id == 1
    assert order_dto.created_at == "2023-11-30T09:00:00Z"
    assert order_dto.updated_at == "2023-11-30T12:00:00Z"


def test_output_order_dto_to_dict():
    item_dto = OrderItemDTO(
        id=1,
        product_id=101,
        description="Test Product",
        price=50.0,
        quantity=2,
    )

    order_dto = OutputOrderDTO(
        id=1,
        number="P000001",
        customer_id=123,
        status="PENDING",
        total=100.0,
        items=[item_dto],
        created_at="2023-11-30T09:00:00Z",
        updated_at="2023-11-30T12:00:00Z",
    )

    order_dict = order_dto.to_dict()

    assert order_dict["id"] == 1
    assert order_dict["number"] == "P000001"
    assert order_dict["customer_id"] == 123
    assert order_dict["status"] == "PENDING"
    assert order_dict["total"] == 100.0
    assert len(order_dict["items"]) == 1
    assert order_dict["created_at"] == "2023-11-30T09:00:00Z"
    assert order_dict["updated_at"] == "2023-11-30T12:00:00Z"
