from datetime import datetime
from typing import Dict, List
from domain.entities import OrderEntity, OrderItemEntity, OrderStatus
from domain.exceptions import EntityNotFoundException
from domain.parameters import OrderFilters
from ports.repositories import OrderRepositoryInterface


class OrderService:

    def __init__(self, order_repository: OrderRepositoryInterface):
        self._order_repository = order_repository

    def register_order(
        self, customer_id: int, items: Dict, total: float
    ) -> OrderEntity:

        items = [self._prepare_order_item(item) for item in items]

        last_order_sequence = self._order_repository.get_last_order_sequence()
        if not last_order_sequence:
            last_order_sequence = self._order_repository.save_order_sequence(
                last_order_id=0
            )
        new_last_number = last_order_sequence.last_order_id + 1
        self._order_repository.save_order_sequence(last_order_id=new_last_number)
        order_sequence_id_str = f"P{new_last_number:06d}"

        order = OrderEntity(
            customer_id=customer_id,
            items=items,
            total=total,
            number=order_sequence_id_str,
        )

        return self._order_repository.create(order_entity=order)

    def find_all_order(self, filters: OrderFilters) -> List[OrderEntity]:
        orders = self._order_repository.list(filters=filters)
        if not orders:
            raise EntityNotFoundException("No orders found.")
        return orders

    def update_status_order(self, order_id: int, status: OrderStatus) -> OrderEntity:
        updated_at = datetime.now()
        order = self._order_repository.patch(
            order_id=order_id, updated_at=updated_at, status=status
        )
        if not order:
            raise EntityNotFoundException("Product not found.")
        return order

    def _prepare_order_item(self, item: Dict) -> OrderItemEntity:
        return OrderItemEntity(
            product_id=item.get("product_id"),
            price=item.get("price"),
            description=item.get("description"),
            quantity=item.get("quantity"),
        )
