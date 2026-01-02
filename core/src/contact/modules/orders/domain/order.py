from dataclasses import dataclass
from datetime import datetime
from .order_status import OrderStatus


@dataclass
class Order:
    contact_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime

