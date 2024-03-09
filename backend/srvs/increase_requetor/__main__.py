from backend.adapters.core import Core
from backend.libs.rabbit import RabbitAdapter
from backend.libs.redis import RedisAdapter
from backend.srvs.increase_requetor.settings import (
    RABBIT_URL,
    QUEUE,
    REDIS_URL,
    CORE_BASE_URL,
)

core_adapter = Core(
    base_url=CORE_BASE_URL,
)

rabbit = RabbitAdapter(
    url=RABBIT_URL,
    queue=QUEUE,
)

db = RedisAdapter(
    url=REDIS_URL,
)


def callback(request):
    account_id = request["account_id"]
    amount = request["amount"]
    token = request["token"]
    request_id = request["request_id"]

    response = core_adapter.increase(account_id, amount, token)
    if response.ok:
        db.set(request_id, "COMPLETED")
    else:
        db.set(request_id, {"status": "FAILED", "message": response.text})


def main():
    rabbit.consume(callback=callback)


if __name__ == "__main__":
    main()
