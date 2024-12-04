from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict, field


class OrderStatus(Enum):
    PENDING = 1
    RECEIVED = 2
    IN_PREPARATION = 3
    READY = 4
    COMPLETED = 5

    @classmethod
    def from_value(cls, value):
        return cls(value=value)


@dataclass(slots=True)
class OrderItemEntity:
    id: int = field(default=None, repr=False, kw_only=True)
    product_id: int
    price: float
    description: str
    quantity: int
    created_at: datetime = field(default=datetime.now(), kw_only=True)
    updated_at: datetime = field(default=None, kw_only=True)

    @classmethod
    def from_dict(cls, data: Dict):
        data_copy = data
        return cls(**data_copy)


@dataclass(slots=True)
class OrderEntity:
    id: int = field(default=None, repr=False, kw_only=True)
    number: str
    customer_id: int
    items: List[OrderItemEntity]
    total: float
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default=datetime.now(), kw_only=True)
    updated_at: datetime = field(default=None, kw_only=True)

    def add_item(
        self, product_id: int, quantity: int, price: float, description: str = ""
    ):
        order_item = OrderItemEntity(
            product_id=product_id,
            quantity=quantity,
            description=description,
            price=price,
        )
        self.items.append(order_item)

    def as_dict(self) -> Dict:
        serialized = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
        return serialized

    @classmethod
    def from_dict(cls, data: Dict):
        data_copy = data
        data_copy["status"] = OrderStatus(data["status"])
        data_copy["items"] = [OrderItemEntity.from_dict(item) for item in data["items"]]
        return cls(**data_copy)


@dataclass(slots=True)
class OrderSequenceEntity:
    last_order_id: int

    def as_dict(self) -> Dict:
        serialized = asdict(
            self, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
        return serialized

    @classmethod
    def from_dict(cls, data: Dict):
        data_copy = data
        return cls(**data_copy)
