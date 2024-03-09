import json

import redis as _redis
from typing_extensions import (
    Self,
)
from datetime import timedelta


class RedisAdapter:
    def __init__(self: Self, url: str) -> None:
        self.client = _redis.Redis.from_url(
            url=url,
        )

    def get(self: Self, name: str) -> dict | None:
        value_bytes = self.client.get(name)

        value = None
        if value_bytes:
            value = json.loads(value_bytes)

        return value

    def set(self: Self, name: str, value: dict) -> bool:
        _value = json.dumps(value)
        if self.client.set(name, _value):
            return True
        return False

    def set_ttl(self: Self, name: str, value: dict) -> bool:
        _value = json.dumps(value)
        if self.client.set(name, _value, ex=timedelta(hours=2)):
            return True
        return False

    def delete(self: Self, name: str) -> bool:
        if self.client.delete(name):
            return True
        return False
