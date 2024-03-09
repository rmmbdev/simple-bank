from pydantic import (
    BaseModel,
    Extra,
    UUID4,
)


class PydanticValidator(BaseModel, extra=Extra.forbid):
    pass


class HeaderValidator(BaseModel):
    authorization: str


class IncrementQueryValidator(PydanticValidator):
    account_id: UUID4


class IncrementBodyValidator(PydanticValidator):
    amount: float


class GetRequestQueryValidator(PydanticValidator):
    request_id: UUID4


class TransferBodyValidator(PydanticValidator):
    source: UUID4
    destination: UUID4
    amount: float
