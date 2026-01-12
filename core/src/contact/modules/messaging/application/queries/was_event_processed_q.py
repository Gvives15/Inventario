from contact.modules.messaging.infrastructure.orm.message_event_repo import was_event_processed


def execute(provider: str, external_event_id: str) -> bool:
    return was_event_processed(provider, external_event_id)

