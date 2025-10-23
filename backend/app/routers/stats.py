from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.enums import PerfilEnum
from app.schemas.stats import Estatistica
from app.security.auth import require_roles
from app.services.ocorrencia_service import get_estatisticas

router = APIRouter(prefix="/stats", tags=["stats"])

read_permission = require_roles(PerfilEnum.ADMIN, PerfilEnum.USER)


@router.get("/incidents", response_model=Estatistica)
def estatisticas(
    db: Session = Depends(get_db),
    _: None = Depends(read_permission),
):
    payload = get_estatisticas(db)
    return Estatistica(**payload)
