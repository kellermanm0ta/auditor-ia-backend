import json

from sqlalchemy.orm import Session

from app.models.config import Config
from app.schemas.config import ConfigUpdate


class ConfigService:
    def __init__(self, db: Session):
        self.db = db

    def get(self) -> Config | None:
        return self.db.get(Config, 1)

    def get_or_create_default(self) -> Config:
        config = self.db.get(Config, 1)
        if not config:
            config = Config(
                id=1,
                execution_mode="Paralelo",
                output_format_id=1,
                skill_ids=json.dumps(["seguranca", "arquitetura", "codesmell"]),
            )
            self.db.add(config)
            self.db.commit()
            self.db.refresh(config)
        return config

    def update(self, data: ConfigUpdate) -> Config | None:
        config = self.db.get(Config, 1)
        if not config:
            return None
        vals = data.model_dump(exclude_unset=True, by_alias=False)
        if "skill_ids" in vals:
            vals["skill_ids"] = json.dumps(vals["skill_ids"])
        for field, value in vals.items():
            setattr(config, field, value)
        self.db.commit()
        self.db.refresh(config)
        return config
