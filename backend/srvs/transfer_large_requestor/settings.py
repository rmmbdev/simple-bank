from environs import (
    Env,
)

env = Env()
env.read_env()

RABBIT_URL = env.str("RABBIT_URL", "amqp://guest:guest@127.0.0.1:5672/")
QUEUE = env.str("QUEUE", "transfer-large")
REDIS_URL = env.str("REDIS_URL", "redis://localhost:6379/0")
CORE_BASE_URL = env.str("CORE_BASE_URL", "http://localhost:8000")
