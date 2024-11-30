from typing import Optional, List, Dict
from abc import ABC, abstractmethod

from domain.entities import OrderEntity, OrderSequenceEntity
from domain.parameters import OrderFilters


class OrderRepositoryInterface(ABC):

    @abstractmethod
    def create(self, order_entity: OrderEntity) -> Optional[OrderEntity]:
        raise NotImplementedError

    @abstractmethod
    def list(self, filters: OrderFilters) -> List[OrderEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[OrderEntity] | None:
        raise NotImplementedError

    @abstractmethod
    def patch(self, order_id: int, **fields) -> Optional[OrderEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_last_order_sequence(self) -> OrderSequenceEntity | None:
        raise NotImplementedError

    def save_order_sequence(self, last_order_id: int) -> OrderSequenceEntity:
        raise NotImplementedError
