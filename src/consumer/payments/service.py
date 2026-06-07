from src.consumer.payments.repository import PaymentsRepository


class PaymentsService:
    def __init__(self, repository: PaymentsRepository):
        self._repository = repository

    async def process_payment(self):
        pass
