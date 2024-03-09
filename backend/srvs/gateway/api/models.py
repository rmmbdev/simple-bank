from pydantic import (
    BaseModel,
    Extra,
    UUID4,
)


class PydanticValidator(BaseModel, extra=Extra.forbid):
    pass


class HeaderValidator(BaseModel):
    Authorization: str


class IncrementQueryValidator(PydanticValidator):
    account_id: UUID4


class IncrementBodyValidator(PydanticValidator):
    amount: float
