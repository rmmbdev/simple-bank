from environs import (
    Env,
)

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", False)
PORT = env.int("PORT", 8001)

CORE_BASE_URL = env.str("CORE_BASE_URL", "http://localhost:8000")
