import asyncio
import logging
import random
import aiohttp

from faststream.rabbit import RabbitMessage

from src.consumer.payments.repository import PaymentsRepository
from src.consumer.payments.schemes import Payment
from src.core import consts
from src.core.database.models.payment import PaymentStatusType

logger = logging.getLogger(__name__)


class PaymentsService:
    def __init__(self, repository: PaymentsRepository):
        self._repository = repository

    async def process_payment(self, payment: Payment, msg: RabbitMessage) -> None:
        if await self._repository.exists_duplicate_payment_by_idempotency_key(idempotency_key=payment.idempotency_key):
            logger.info("Duplicate payment")
            return

        await asyncio.sleep(random.randint(2, 5))  # Бурная деятельность!

        if random.random() < 0:
            await self.__send_webhook_notification(payment=payment)
            await self._repository.update_payment_status(payment_id=payment.id, status=PaymentStatusType.SUCCEEDED)
            await msg.ack()  # Он конечно и сам с этим справился бы, но я решил помочь ;)
        else:
            delivery_count = msg.headers.get("x-delivery-count")
            logger.info(f"BAD CASE! Attempts: {delivery_count}")
            if delivery_count == consts.DELIVERY_LIMIT:
                await self._repository.update_payment_status(payment_id=payment.id, status=PaymentStatusType.FAILED)

            await msg.nack(requeue=True)

    @staticmethod
    async def __send_webhook_notification(payment: Payment) -> None:
        # По хорошему для этого должен быть отдельный интерфейс для управления вебхуком, но не будем усложнять
        if not payment.webhook_url:
            return

        payload = {
            "status": payment.status,
            "amount": payment.sum,
            "currency": payment.currency,
            "description": payment.description,
            "idempotency_key": payment.idempotency_key,
        }

        timeout = aiohttp.ClientTimeout(total=5, connect=2)
        max_retries = 3
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for attempt in range(1, max_retries + 1):
                try:
                    async with session.post(str(payment.webhook_url), json=payload) as response:
                        if 200 <= response.status < 300:
                            return

                        logger.warning(
                            "Webhook failed (attempt=%s) payment_id=%s status=%s",
                            attempt,
                            payment.id,
                            response.status,
                        )
                except aiohttp.ClientError as e:
                    logger.error(
                        "Webhook request error (attempt=%s) payment_id=%s error=%s",
                        attempt,
                        payment.id,
                        str(e),
                    )

                if attempt < max_retries:
                    await asyncio.sleep(attempt * 2)
