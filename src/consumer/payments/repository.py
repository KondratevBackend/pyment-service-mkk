from src.core.database import Database


class PaymentsRepository:
    def __init__(self, database: Database):
        self._database = database
