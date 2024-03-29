from environs import (
    Env,
)

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", False)
PORT = env.int("PORT", 8001)

CORE_BASE_URL = env.str("CORE_BASE_URL", "http://localhost:8000")
RABBIT_URL = env.str("RABBIT_URL", "amqp://guest:guest@127.0.0.1:5672/")
INCREMENT_QUEUE = env.str("INCREMENT_QUEUE", "increment")
TRANSFER_SMALL_QUEUE = env.str("TRANSFER_SMALL_QUEUE", "transfer-small")
TRANSFER_LARGE_QUEUE = env.str("TRANSFER_LARGE_QUEUE", "transfer-large")
REDIS_URL = env.str("REDIS_URL", "redis://localhost:6379/0")
SMALL_AMOUNT_MAX = env.int("SMALL_AMOUNT_MAX", 10_000_000)
