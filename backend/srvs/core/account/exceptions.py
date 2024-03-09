from rest_framework import (
    status,
)
from rest_framework.exceptions import (
    APIException,
)


class DailyIncrementLimitException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "reached daily increment limit"
    default_code = "daily_increment_limit"


class SourceDestinationEqualException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "source and destination of a transfer can not be the same"
    default_code = "source_destination_equal"


class InsufficientBalanceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "insufficient balance"
    default_code = "insufficient_balance"
