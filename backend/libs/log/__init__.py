import logging
import sys

log = logging.getLogger("SUN")
log.setLevel(logging.DEBUG)

datefmt = "%Y-%m-%dT%H:%M:%S%z"  # ISO 8601
formatter = logging.Formatter(
    "%(asctime)s:%(name)s:%(levelname)s:%(message)s",
    datefmt=datefmt,
)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
log.addHandler(handler)
