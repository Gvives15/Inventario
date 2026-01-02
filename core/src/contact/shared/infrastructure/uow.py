from contextlib import AbstractContextManager
from django.db import transaction
from contact.modules.conversations.infrastructure.orm import contact_repo, conversation_repo, message_inbound_repo
from contact.modules.orders.infrastructure.orm import order_repo


class UnitOfWork(AbstractContextManager):
    def __init__(self):
        self.contacts = contact_repo
        self.conversations = conversation_repo
        self.orders = order_repo
        self.inbound = message_inbound_repo
        self._ctx = None

    def __enter__(self):
        self._ctx = transaction.atomic()
        self._ctx.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._ctx:
            self._ctx.__exit__(exc_type, exc, tb)
        return False
