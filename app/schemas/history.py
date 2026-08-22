from datetime import datetime

from pydantic import BaseModel


class HistoryBase(BaseModel):
    repo: str
    date: datetime
    issues: int = 0
    severity: str
    agents: int = 0
    time: str


class HistoryCreate(HistoryBase):
    pass


class HistoryUpdate(BaseModel):
    repo: str | None = None
    date: datetime | None = None
    issues: int | None = None
    severity: str | None = None
    agents: int | None = None
    time: str | None = None


class HistoryResponse(HistoryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
