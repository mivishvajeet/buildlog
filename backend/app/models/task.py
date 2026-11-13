import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.milestone import Milestone


class Task(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'blocked', 'done', 'cancelled')",
            name="ck_tasks_status",
        ),
        CheckConstraint("priority IN ('low', 'medium', 'high')", name="ck_tasks_priority"),
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    milestone_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("milestones.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="todo")
    priority: Mapped[str] = mapped_column(String(10), nullable=False, default="medium")
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    project: Mapped["Project"] = relationship(back_populates="tasks")
    milestone: Mapped["Milestone | None"] = relationship(back_populates="tasks")
