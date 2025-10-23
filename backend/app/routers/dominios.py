from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.enums import PerfilEnum, PrioridadeEnum, StatusEnum
from app.schemas.common import Dominio
from app.security.auth import require_roles

router = APIRouter(prefix="/dominios", tags=["dominios"])

read_permission = require_roles(PerfilEnum.ADMIN, PerfilEnum.USER)


def _to_dominio(enum_cls):
    return [Dominio(code=item.value, label=item.label) for item in enum_cls]


@router.get("/status", response_model=list[Dominio])
def listar_status(_: None = Depends(read_permission)):
    return _to_dominio(StatusEnum)


@router.get("/prioridades", response_model=list[Dominio])
def listar_prioridades(_: None = Depends(read_permission)):
    return _to_dominio(PrioridadeEnum)


@router.get("/perfis", response_model=list[Dominio])
def listar_perfis(_: None = Depends(read_permission)):
    return _to_dominio(PerfilEnum)
