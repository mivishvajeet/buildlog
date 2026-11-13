from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project_repository import ProjectRepository


class Repository(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "repositories"

    github_repository_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    owner_login: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(201), unique=True, nullable=False)
    default_branch: Mapped[str | None] = mapped_column(String(255), nullable=True)
    visibility: Mapped[str] = mapped_column(String(20), nullable=False, default="private")
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    html_url: Mapped[str] = mapped_column(String(500), nullable=False)
    last_synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    project_links: Mapped[list["ProjectRepository"]] = relationship(
        back_populates="repository", cascade="all, delete-orphan"
    )
