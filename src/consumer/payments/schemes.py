import pydantic

from src.core.database.models.payment import CurrencyType, PaymentStatusType


class Payment(pydantic.BaseModel):
    id: int  # or pydantic.Field(..., description="...")
    sum: int
    currency: CurrencyType
    description: str | None = None  # or pydantic.Filed(None, description="...", )
    meta_data: pydantic.JsonValue | None = None
    status: PaymentStatusType
    webhook_url: pydantic.HttpUrl | None = None
    idempotency_key: pydantic.UUID4

