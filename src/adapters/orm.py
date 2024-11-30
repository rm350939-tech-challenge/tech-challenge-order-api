import os
from typing import Dict, List, Optional
from datetime import datetime

from playhouse.shortcuts import model_to_dict
from peewee import (
    PostgresqlDatabase,
    Model,
    CharField,
    DecimalField,
    ForeignKeyField,
    DateTimeField,
    SmallIntegerField,
    IntegerField,
    TextField,
    SQL,
)

from domain.entities import (
    OrderEntity,
    OrderItemEntity,
    OrderSequenceEntity,
    OrderStatus,
)
from domain.parameters import OrderFilters
from ports.repositories import OrderRepositoryInterface

db = PostgresqlDatabase(
    database=os.environ.get("DATABASE_NAME"),
    host=os.environ.get("DATABASE_HOST"),
    port=os.environ.get("DATABASE_PORT"),
    user=os.environ.get("DATABASE_USER"),
    password=os.environ.get("DATABASE_PASSWORD"),
)


class OrderModel(Model):
    number: str = CharField()
    customer_id: int = IntegerField()
    status: int = SmallIntegerField()
    total: float = DecimalField()
    created_at: datetime = DateTimeField()
    updated_at: datetime = DateTimeField(null=True)

    def model_to_dict(self) -> Dict:
        return model_to_dict(self, backrefs=True)

    class Meta:
        database = db
        table_name = "orders"
        schema = os.environ.get("DATABASE_SCHEMA_NAME")


class OrderItemModel(Model):
    product_id: int = IntegerField()
    order: int = ForeignKeyField(OrderModel, backref="items")
    price: float = DecimalField()
    description = TextField()
    quantity: float = DecimalField()

    def model_to_dict(self) -> Dict:
        return model_to_dict(self)

    class Meta:
        database = db
        table_name = "order_items"
        schema = os.environ.get("DATABASE_SCHEMA_NAME")


class OrderSequenceModel(Model):
    last_order_id: int = IntegerField()

    def model_to_dict(self) -> Dict:
        return model_to_dict(self)

    class Meta:
        database = db
        table_name = "order_sequences"
        schema = os.environ.get("DATABASE_SCHEMA_NAME")


class OrderRepository(OrderRepositoryInterface):

    def create(self, order_entity: OrderEntity) -> OrderEntity:
        order = OrderModel.create(
            number=order_entity.number,
            customer=order_entity.customer.id,
            status=order_entity.status.value,
            total=order_entity.total,
            created_at=order_entity.created_at,
        )
        for item in order_entity.items:
            order_item = OrderItemModel(
                product=item.product.id, price=item.price, quantity=item.quantity
            )
            order_item.order = order
            order_item.save()
        return OrderEntity.from_dict(order.model_to_dict())

    def list(self, filters: OrderFilters) -> List[OrderEntity]:
        where = (
            OrderModel.status.in_(
                [OrderStatus[status].value for status in filters.status]
            ),
        )

        if filters.customer_id:
            where += (OrderModel.customer == filters.customer_id,)

        orders = (
            OrderModel.select()
            .where(*where)
            .order_by(SQL(f"{filters.sort} {filters.order}, id {filters.order}"))
        )

        return [OrderEntity.from_dict(order.model_to_dict()) for order in orders]

    def get_by_id(self, order_id: int) -> Optional[OrderEntity] | None:
        order = OrderModel.get_or_none(id=order_id)
        if not order:
            return None
        return OrderEntity.from_dict(order.model_to_dict())

    def patch(self, order_id: int, **fields) -> Optional[OrderEntity] | None:
        order = OrderModel.get_or_none(id=order_id)
        if not order:
            return None
        for key, value in fields.items():
            if hasattr(OrderEntity, key):
                setattr(order, key, value)
        updated_order = OrderEntity.from_dict(order.model_to_dict())
        order.save()
        return updated_order

    def get_last_order_sequence(self) -> OrderSequenceEntity | None:
        order_sequence = (
            OrderSequenceModel.select().order_by(OrderSequenceModel.id.desc()).first()
        )
        if not order_sequence:
            return None
        return OrderSequenceEntity.from_dict(order_sequence.model_to_dict())

    def save_order_sequence(self, last_order_id: int) -> OrderSequenceEntity:
        order_sequence = OrderSequenceModel.create(last_order_id=last_order_id)
        return OrderSequenceEntity.from_dict(order_sequence.model_to_dict())
