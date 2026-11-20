from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.auth import get_current_user
from api.database import get_db
from api.models import User, AnalysisHistory


router = APIRouter(prefix="/history", tags=["User History"])


def save_analysis(
    db: Session,
    user: User,
    result: dict,
    source: str,
    input_text: str | None = None,
    input_url: str | None = None,
    filename: str | None = None,
):
    """Save a completed analysis for an authenticated user."""

    record = AnalysisHistory(
        user_id=user.id,
        source=source,
        title=result.get("title") or None,
        input_text=input_text,
        input_url=input_url,
        filename=filename,
        prediction=result["prediction"],
        label=result.get("label"),
        decision_score=result.get("decision_score"),
        result=result,
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception:
        db.rollback()
        raise


@router.get("/")
def get_history(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    source: str | None = Query(default=None, pattern="^(text|pdf|url)$"),
    prediction: str | None = Query(default=None, pattern="^(REAL|FAKE)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(AnalysisHistory).filter(
        AnalysisHistory.user_id == current_user.id
    )

    if source:
        query = query.filter(AnalysisHistory.source == source)

    if prediction:
        query = query.filter(AnalysisHistory.prediction == prediction)

    total = query.count()

    records = (
        query.order_by(AnalysisHistory.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": records,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
    }


@router.get("/stats")
def get_history_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    base_query = db.query(AnalysisHistory).filter(
        AnalysisHistory.user_id == current_user.id
    )

    total = base_query.count()

    real_count = (
        db.query(func.count(AnalysisHistory.id))
        .filter(
            AnalysisHistory.user_id == current_user.id,
            AnalysisHistory.prediction == "REAL",
        )
        .scalar()
    )

    fake_count = (
        db.query(func.count(AnalysisHistory.id))
        .filter(
            AnalysisHistory.user_id == current_user.id,
            AnalysisHistory.prediction == "FAKE",
        )
        .scalar()
    )

    return {
        "total_analyses": total,
        "real_count": real_count,
        "fake_count": fake_count,
    }


@router.get("/{analysis_id}")
def get_history_item(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(AnalysisHistory)
        .filter(
            AnalysisHistory.id == analysis_id,
            AnalysisHistory.user_id == current_user.id,
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis record not found.",
        )

    return record


@router.delete("/{analysis_id}")
def delete_history_item(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(AnalysisHistory)
        .filter(
            AnalysisHistory.id == analysis_id,
            AnalysisHistory.user_id == current_user.id,
        )
        .first()
    )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis record not found.",
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Analysis history deleted successfully.",
        "deleted_id": analysis_id,
    }
