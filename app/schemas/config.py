import json

from pydantic import BaseModel, field_validator
from pydantic.alias_generators import to_camel


class ConfigBase(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    execution_mode: str = "Paralelo"
    output_format_id: int
    skill_ids: list[str]


class ConfigUpdate(BaseModel):
    model_config = {"alias_generator": to_camel, "populate_by_name": True}

    execution_mode: str | None = None
    output_format_id: int | None = None
    skill_ids: list[str] | None = None


class ConfigResponse(ConfigBase):
    id: int

    model_config = {"alias_generator": to_camel, "populate_by_name": True, "from_attributes": True}

    @field_validator("skill_ids", mode="before")
    @classmethod
    def parse_skill_ids(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
