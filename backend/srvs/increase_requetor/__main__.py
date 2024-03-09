from backend.libs.rabbit import RabbitAdapter
from backend.libs.redis import RedisAdapter
from backend.srvs.increase_requetor.settings import (
    RABBIT_URL,
    QUEUE,
    REDIS_URL,
)

rabbit = RabbitAdapter(
    url=RABBIT_URL,
    queue=QUEUE,
)

db = RedisAdapter(
    url=REDIS_URL,
)
