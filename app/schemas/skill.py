from pydantic import BaseModel


class SkillBase(BaseModel):
    id: str
    name: str
    icon: str
    desc: str
    enabled: bool = False
    prompt: str


class SkillCreate(SkillBase):
    pass


class SkillUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    desc: str | None = None
    enabled: bool | None = None
    prompt: str | None = None


class SkillResponse(SkillBase):
    model_config = {"from_attributes": True}
