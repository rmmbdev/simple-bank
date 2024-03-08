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
