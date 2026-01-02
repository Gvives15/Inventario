from dataclasses import dataclass
from datetime import datetime


@dataclass
class Contact:
    whatsapp_id: str
    name: str
    zone: str
    business_type: str
    created_at: datetime
    updated_at: datetime

