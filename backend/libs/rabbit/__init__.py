import json
from collections.abc import (
    Callable,
)
from time import (
    sleep,
)

import pika
from pika import (
    spec,
)
from pika.adapters.blocking_connection import (
    BlockingChannel,
    BlockingConnection,
)
from pika.exceptions import (
    AMQPConnectionError,
)
from typing_extensions import (
    Self,
)

from backend.libs.log import (
    log,
)


class RabbitAdapter:
    reconnect_delay: int = 3
    exchange: str = ""
    _declare: bool = False
    _channel: BlockingChannel
    _connection: BlockingConnection
    _queue: str
    _dl_queue: str

    def __init__(self: Self, url: str, queue: str) -> None:
        self._connection_parameters = pika.URLParameters(url)
        self._queue = queue

    def declare(self: Self) -> None:
        self._channel.exchange_declare(
            exchange="dlx",
            exchange_type="direct",
            durable=True,
        )

        delay_queue = self._queue + "-delay"
        delay_queue_args = {
            "x-message-ttl": 5000,
            "x-dead-letter-exchange": "amq.direct",
            "x-dead-letter-routing-key": self._queue,
        }
        self._channel.queue_declare(
            queue=delay_queue,
            durable=True,
            arguments=delay_queue_args,
        )
        self._channel.queue_bind(exchange="dlx", queue=delay_queue)

        self._dl_queue = self._queue + "-dl"
        self._channel.queue_declare(queue=self._dl_queue, durable=True)
        self._channel.queue_bind(exchange="dlx", queue=self._dl_queue)

        queue_args = {
            "x-dead-letter-exchange": "dlx",
            "x-dead-letter-routing-key": delay_queue,
        }
        self._channel.queue_declare(
            queue=self._queue,
            durable=True,
            arguments=queue_args,
        )
        self._channel.queue_bind(exchange="amq.direct", queue=self._queue)

    def connect(self: Self) -> None:
        while True:
            try:
                self._connection = BlockingConnection(
                    self._connection_parameters,
                )
                self._channel = self._connection.channel()

                if not self._declare:
                    self.declare()
                    self._declare = True

                break
            except AMQPConnectionError:
                log.error("AMQP connection error")
                log.info(f"Reconnect after {self.reconnect_delay} seconds")
                sleep(self.reconnect_delay)

    @property
    def channel(self: Self) -> BlockingChannel:
        if not hasattr(self, "_channel"):
            self.connect()

        return self._channel

    def publish(self: Self, message: dict) -> None:
        message_str = json.dumps(message)
        message_bytes = message_str.encode(encoding="utf-8")

        while True:
            try:
                self.channel.basic_publish(
                    exchange=self.exchange,
                    routing_key=self._queue,
                    body=message_bytes,
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                    ),
                )
                break
            except AMQPConnectionError:
                self.connect()

    def consume(self: Self, callback: Callable[[dict], None]) -> None:
        def _callback(
            channel: BlockingChannel,
            method: spec.Basic.Deliver,
            properties: spec.BasicProperties,
            body: bytes,
        ):
            body_str = body.decode(encoding="utf-8")
            body_dict = json.loads(body_str)

            try:
                callback(body_dict)
                channel.basic_ack(method.delivery_tag)
            except Exception as e:
                log.error(
                    f"queue={method.routing_key} message={body_str} error={e}",
                )
                if not properties.headers or (
                    properties.headers.get("x-death") is None
                    or properties.headers.get("x-death")[0].get("count") < 5
                ):
                    log.info("Message sent to delay queue")
                    channel.basic_reject(method.delivery_tag, requeue=False)
                else:
                    log.info("Message sent to dead queue")
                    channel.basic_publish(
                        exchange="dlx",
                        routing_key=self._dl_queue,
                        body=body,
                        properties=pika.BasicProperties(
                            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                        ),
                    )
                    channel.basic_ack(delivery_tag=method.delivery_tag)

        while True:
            try:
                self.channel.basic_qos(prefetch_count=1)
                self.channel.basic_consume(
                    queue=self._queue,
                    on_message_callback=_callback,
                    auto_ack=False,
                )
                self.channel.start_consuming()
                break
            except AMQPConnectionError:
                self.connect()
