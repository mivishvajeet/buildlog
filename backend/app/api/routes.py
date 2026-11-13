from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db

router = APIRouter()


@router.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Liveness probe: the API process is responding."""
    return {"status": "ok", "service": "buildlog-api"}


@router.get("/health/ready", tags=["system"])
def readiness_check(db: Session = Depends(get_db)) -> dict[str, str]:
    """Readiness probe: the API can reach its database."""
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc

    return {"status": "ready", "database": "ok"}
