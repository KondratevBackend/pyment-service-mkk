from faststream.rabbit import RabbitExchange, ExchangeType

payment_exchange = RabbitExchange("payments", type=ExchangeType.DIRECT, durable=True)
