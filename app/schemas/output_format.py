from pydantic import BaseModel


class OutputFormatBase(BaseModel):
    value: str
    label: str


class OutputFormatCreate(OutputFormatBase):
    pass


class OutputFormatUpdate(BaseModel):
    value: str | None = None
    label: str | None = None


class OutputFormatResponse(OutputFormatBase):
    id: int

    model_config = {"from_attributes": True}
