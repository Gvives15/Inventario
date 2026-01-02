from enum import Enum


class ConversationStage(Enum):
    E0_NEW = "E0_NEW"
    E1_MIN_DATA = "E1_MIN_DATA"
    E2_PROPOSAL = "E2_PROPOSAL"
    E3_ADJUST = "E3_ADJUST"
    E4_CONFIRMED = "E4_CONFIRMED"

