from django.conf import (
    settings,
)

if not hasattr(settings, "ACCOUNT"):
    settings.ACCOUNT = {}

AMOUNT_MAX_DIGITS = settings.ACCOUNT.get("AMOUNT_MAX_DIGITS")
AMOUNT_DECIMAL_PLACES = settings.ACCOUNT.get("AMOUNT_DECIMAL_PLACES")
INITIAL_AMOUNT = settings.ACCOUNT.get("INITIAL_AMOUNT")
DAILY_INCREMENT_LIMIT = settings.ACCOUNT.get("DAILY_INCREMENT_LIMIT")
