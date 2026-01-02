from django.db import transaction

class UnitOfWork:
    def __enter__(self):
        self.tx = transaction.atomic()
        self.tx.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tx.__exit__(exc_type, exc_val, exc_tb)
