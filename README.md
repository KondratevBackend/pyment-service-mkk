## Запуск
1. Создайте файл `.env` на основе примера:

```bash
cp .env-example .env
```

2. Запустите приложение:

```bash
docker compose up -d --build
```

После запуска API будет доступно по адресу:

```
http://localhost:8000
```

## Тестируем!
### Минимальный платеж

```bash
curl -X POST \
  'http://localhost:8000/v1/payments' \
  -H 'accept: application/json' \
  -H 'Idempotency-Key: 78ea4b69-f280-4afb-810b-67dbdbfdf994' \
  -H 'X-API-KEY: salt-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "sum": 10000,
    "currency": "RUB"
}'
```

### Платеж с webhook

```bash
curl -X POST \
  'http://localhost:8000/v1/payments' \
  -H 'accept: application/json' \
  -H 'Idempotency-Key: ac376574-7d46-4e70-8b64-2c232fd9f598' \
  -H 'X-API-KEY: salt-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "sum": 500,
    "currency": "RUB",
    "description": "Покупка",
    "webhook_url": "http://localhost:8000/v1/payments/13"
}'
```

### Платеж с метаданными

```bash
curl -X POST \
  'http://localhost:8000/v1/payments' \
  -H 'accept: application/json' \
  -H 'Idempotency-Key: 90bfd5d0-8590-45b3-95f3-7237e4c1fe72' \
  -H 'X-API-KEY: salt-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "sum": 5000,
    "currency": "USD",
    "description": "Оплата заказа №12345",
    "meta_data": {
      "order_id": "ORD-12345",
      "user_id": 42,
      "items": ["товар1", "товар2"]
    },
    "webhook_url": "https://api.myshop.com/webhooks/payment"
}'
```

### Ещё один платеж

```bash
curl -X POST \
  'http://localhost:8000/v1/payments' \
  -H 'accept: application/json' \
  -H 'Idempotency-Key: a8d20b8e-7894-4c8e-8898-97f9ddf8ad87' \
  -H 'X-API-KEY: salt-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "sum": 150000,
    "currency": "RUB",
    "webhook_url": "https://payment-processor.example.com/callback"
}'
```
