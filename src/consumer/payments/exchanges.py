from faststream.rabbit import ExchangeType, RabbitExchange

payment_exchange = RabbitExchange("payments", type=ExchangeType.DIRECT, durable=True)
