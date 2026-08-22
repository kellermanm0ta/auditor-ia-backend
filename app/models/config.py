from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Config(Base):
    __tablename__ = "config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    execution_mode: Mapped[str] = mapped_column(String(20), nullable=False, default="Paralelo")
    output_format_id: Mapped[int] = mapped_column(Integer, nullable=False)
    skill_ids: Mapped[str] = mapped_column(Text, nullable=False)
