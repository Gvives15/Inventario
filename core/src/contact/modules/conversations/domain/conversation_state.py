from dataclasses import dataclass
from datetime import datetime
from .conversation_stage import ConversationStage


@dataclass
class ConversationState:
    contact_id: int
    stage: ConversationStage
    last_order_id: int | None
    updated_at: datetime

