from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ProjectStatus = Literal["idea", "planned", "active", "paused", "completed", "archived"]
ProjectVisibility = Literal["private", "public"]


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    category: str | None = Field(default=None, max_length=80)
    description: str | None = Field(default=None, max_length=10000)
    status: ProjectStatus = "idea"
    visibility: ProjectVisibility = "private"
    started_on: date | None = None
    target_date: date | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Project name cannot be blank")
        return value

    @field_validator("category", "description")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.started_on and self.target_date and self.target_date < self.started_on:
            raise ValueError("Target date cannot be earlier than the start date")
        return self


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    category: str | None = Field(default=None, max_length=80)
    description: str | None = Field(default=None, max_length=10000)
    status: ProjectStatus | None = None
    visibility: ProjectVisibility | None = None
    started_on: date | None = None
    target_date: date | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Project name cannot be blank")
        return value

    @field_validator("category", "description")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None


class ProjectRead(BaseModel):
    id: UUID
    name: str
    slug: str
    category: str | None
    description: str | None
    status: ProjectStatus
    visibility: ProjectVisibility
    is_published: bool
    started_on: date | None
    target_date: date | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
