from time import sleep

from backend.adapters.core import Core
from backend.libs.rabbit import RabbitAdapter
from backend.libs.redis import RedisAdapter
from backend.srvs.transfer_large_requestor.settings import (
    RABBIT_URL,
    QUEUE,
    REDIS_URL,
    CORE_BASE_URL,
)
from datetime import datetime, timedelta, time

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

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
TIME_PERIODS = [
    (
        (datetime.combine(datetime.today(), time(0, 0, 0)) + timedelta(hours=i * 4)).time(),
        (datetime.combine(datetime.today(), time(0, 0, 0)) + timedelta(hours=(i + 1) * 4)).time()
    )
    for i in
    range(6)
]


def callback(request):
    now_time = datetime.now().time()
    period = None
    for tp in TIME_PERIODS:
        if tp[0] <= now_time <= tp[1]:
            period = tp
            break

    source = request["source"]
    destination = request["destination"]
    amount = request["amount"]
    token = request["token"]
    request_id = request["request_id"]
    request_date = datetime.strptime(request["request_date"], DATETIME_FORMAT).time()
    if period[0] < request_date:
        seconds = (
                      datetime.combine(datetime.today(), period[1]) - datetime.combine(datetime.today(), now_time)
                  ).seconds + 1
        sleep(seconds)

    response = core_adapter.transfer(source=source, destination=destination, amount=amount, token=token)
    if response.ok:
        db.set_ttl(request_id, "COMPLETED")
    else:
        db.set_ttl(request_id, {"status": "FAILED", "message": response.text})


def main():
    rabbit.consume(callback=callback)


if __name__ == "__main__":
    main()
