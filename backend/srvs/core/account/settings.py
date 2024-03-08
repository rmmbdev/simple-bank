from django.conf import (
    settings,
)

if not hasattr(settings, "ACCOUNT"):
    settings.ACCOUNT = {}

AMOUNT_MAX_DIGITS = settings.ACCOUNT.get("AMOUNT_MAX_DIGITS")
AMOUNT_DECIMAL_PLACES = settings.ACCOUNT.get("AMOUNT_DECIMAL_PLACES")
