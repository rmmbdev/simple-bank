from environs import (
    Env,
)

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", False)
PORT = env.int("PORT", 8001)
