import asyncio
import logging
import random

import aiohttp
from faststream.rabbit import RabbitBroker, RabbitMessage

from src.consumer.payments import exchanges
from src.consumer.payments.repository import PaymentsRepository
from src.consumer.payments.schemes import Payment
from src.core import consts
from src.core.database.models.payment import PaymentStatusType

logger = logging.getLogger(__name__)


class PaymentsService:
    def __init__(self, repository: PaymentsRepository):
        self._repository = repository

    async def process_payment(self, payment: Payment, msg: RabbitMessage, broker: RabbitBroker) -> None:
        if await self._repository.exists_duplicate_payment_by_idempotency_key(idempotency_key=payment.idempotency_key):
            logger.info("Duplicate payment")
            return

        await asyncio.sleep(random.randint(2, 5))  # Бурная деятельность!

        if random.random() < 0.9:
            await self.__send_webhook_notification(payment=payment)
            await self._repository.update_payment_status(payment_id=payment.id, status=PaymentStatusType.SUCCEEDED)
        else:
            retry_count = msg.headers.get("x-retry-count", 0) + 1
            logger.info(f"BAD CASE! Attempts: {retry_count}")

            retry_limit = 4
            if retry_count == retry_limit:
                await broker.publish(
                    message=payment,
                    exchange=consts.DEAD_LETTER_EXCHANGE,
                    queue=consts.DEAD_LETTER_QUEUE,
                    routing_key=consts.DEAD_LETTER_ROUTING_KEY,
                    persist=True,
                    headers={
                        **msg.headers,
                        "x-retry-count": retry_count,
                    },
                )
                await self._repository.update_payment_status(payment_id=payment.id, status=PaymentStatusType.FAILED)
                return

            await broker.publish(
                message=payment,
                exchange=exchanges.payment_exchange,
                queue=f"payments.retry.{retry_count}",
                persist=True,
                headers={
                    **msg.headers,
                    "x-retry-count": retry_count,
                },
            )
            await msg.nack(requeue=False)

    @staticmethod
    async def __send_webhook_notification(payment: Payment) -> None:
        # По хорошему для этого должен быть отдельный интерфейс для управления вебхуком
        if not payment.webhook_url:
            return

        payload = {
            "status": payment.status,
            "amount": payment.sum,
            "currency": payment.currency,
            "description": payment.description,
            "idempotency_key": str(payment.idempotency_key),
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
