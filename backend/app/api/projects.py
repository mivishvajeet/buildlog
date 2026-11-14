import re
from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.projects import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


def _make_slug(name: str, user_id: UUID, db: Session, exclude_id: UUID | None = None) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "project"
    candidate = base
    suffix = 2

    while True:
        statement = select(Project.id).where(
            Project.user_id == user_id,
            Project.slug == candidate,
        )
        if exclude_id is not None:
            statement = statement.where(Project.id != exclude_id)
        if db.scalar(statement) is None:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1


def _get_owned_project(project_id: UUID, user_id: UUID, db: Session) -> Project:
    project = db.scalar(
        select(Project).where(Project.id == project_id, Project.user_id == user_id)
    )
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    project = Project(
        user_id=current_user.id,
        name=payload.name,
        slug=_make_slug(payload.name, current_user.id, db),
        category=payload.category,
        description=payload.description,
        status=payload.status,
        visibility=payload.visibility,
        started_on=payload.started_on,
        target_date=payload.target_date,
        completed_at=datetime.now(UTC) if payload.status == "completed" else None,
    )
    db.add(project)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A project with this name already exists",
        ) from exc
    db.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
def list_projects(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Project]:
    statement = (
        select(Project)
        .where(Project.user_id == current_user.id)
        .order_by(Project.updated_at.desc(), Project.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(db.scalars(statement).all())


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    return _get_owned_project(project_id, current_user.id, db)


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    project = _get_owned_project(project_id, current_user.id, db)
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one project field must be provided",
        )

    for required_field in ("name", "status", "visibility"):
        if required_field in changes and changes[required_field] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{required_field} cannot be null",
            )

    if "name" in changes and changes["name"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Project name cannot be null",
        )

    if "name" in changes and changes["name"] is not None:
        project.slug = _make_slug(changes["name"], current_user.id, db, exclude_id=project.id)

    for field, value in changes.items():
        setattr(project, field, value)

    if project.started_on and project.target_date and project.target_date < project.started_on:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Target date cannot be earlier than the start date",
        )

    if "status" in changes:
        if project.status == "completed" and project.completed_at is None:
            project.completed_at = datetime.now(UTC)
        elif project.status != "completed":
            project.completed_at = None

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project update conflicts with an existing record",
        ) from exc
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    project = _get_owned_project(project_id, current_user.id, db)
    db.delete(project)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
