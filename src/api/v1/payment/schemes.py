import datetime

import pydantic

from src.core.database.models.payment import CurrencyType, PaymentStatusType


class PaymentResponse(pydantic.BaseModel):
    payment_id: int = pydantic.Field(..., validation_alias="id")
    sum: int  # or pydantic.Field(..., description="...")
    currency: CurrencyType
    description: str | None = None  # or pydantic.Filed(None, description="...", )
    meta_data: pydantic.JsonValue | None = None
    status: PaymentStatusType
    webhook_url: pydantic.HttpUrl | None = None
    idempotency_key: pydantic.UUID4


class CreatePaymentRequest(pydantic.BaseModel):
    sum: int
    currency: CurrencyType
    description: str | None = None
    meta_data: pydantic.JsonValue | None = None
    webhook_url: pydantic.HttpUrl | None = None


class CreatePaymentResponse(pydantic.BaseModel):
    payment_id: int = pydantic.Field(..., validation_alias="id")
    status: PaymentStatusType
    created_at: datetime.datetime
