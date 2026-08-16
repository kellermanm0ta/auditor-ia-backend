import json
from datetime import datetime

from pydantic import BaseModel, field_validator


class IntegrationBase(BaseModel):
    name: str
    icon: str
    desc: str
    status: str = "disconnected"
    status_label: str
    doc_url: str
    steps: list[str]
    yaml: str


class IntegrationCreate(IntegrationBase):
    pass


class IntegrationUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    desc: str | None = None
    status: str | None = None
    status_label: str | None = None
    doc_url: str | None = None
    steps: list[str] | None = None
    yaml: str | None = None


class IntegrationResponse(IntegrationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @field_validator("steps", mode="before")
    @classmethod
    def parse_steps(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
