from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.enums import PerfilEnum
from app.schemas.comentario import ComentarioCreate, ComentarioOut
from app.schemas.common import PageResponse
from app.schemas.ocorrencia import (
    OcorrenciaCreate,
    OcorrenciaOut,
    OcorrenciaStatusUpdate,
    OcorrenciaUpdate,
)
from app.services import ocorrencia_service
from app.services.ocorrencia_service import OcorrenciaNotFoundError
from app.utils.pagination import build_page
from app.security.auth import require_roles

router = APIRouter(prefix="/incidents", tags=["incidents"])

read_permission = require_roles(PerfilEnum.ADMIN, PerfilEnum.USER)
write_permission = require_roles(PerfilEnum.ADMIN)
create_permission = require_roles(PerfilEnum.ADMIN, PerfilEnum.USER)


@router.get("", response_model=PageResponse[OcorrenciaOut])
def listar(
    page: int = Query(0, ge=0),
    size: int = Query(10, ge=1, le=100),
    sort: str = Query("dataAbertura"),
    direction: str = Query("desc"),
    status: Optional[str] = Query(None),
    prioridade: Optional[str] = Query(None),
    texto: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: None = Depends(read_permission),
):
    try:
        items, total = ocorrencia_service.list_ocorrencias(
            db,
            page=page,
            size=size,
            status=status,
            prioridade=prioridade,
            texto=texto,
            sort_field=sort,
            sort_direction=direction,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    dtos = [OcorrenciaOut.model_validate(item) for item in items]
    return build_page(dtos, total=total, page=page, size=size)


@router.get("/{ocorrencia_id}", response_model=OcorrenciaOut)
def buscar_por_id(
    ocorrencia_id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(read_permission),
):
    try:
        ocorrencia = ocorrencia_service.get_ocorrencia(db, ocorrencia_id)
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return OcorrenciaOut.model_validate(ocorrencia)


@router.post("", response_model=OcorrenciaOut)
def criar(
    payload: OcorrenciaCreate,
    db: Session = Depends(get_db),
    _: None = Depends(create_permission),
):
    try:
        ocorrencia = ocorrencia_service.create_ocorrencia(db, payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return OcorrenciaOut.model_validate(ocorrencia)


@router.put("/{ocorrencia_id}", response_model=OcorrenciaOut)
def atualizar(
    ocorrencia_id: UUID,
    payload: OcorrenciaUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(write_permission),
):
    try:
        ocorrencia = ocorrencia_service.update_ocorrencia(
            db, ocorrencia_id, payload.model_dump()
        )
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return OcorrenciaOut.model_validate(ocorrencia)


@router.patch("/{ocorrencia_id}/status", response_model=OcorrenciaOut)
def alterar_status(
    ocorrencia_id: UUID,
    payload: OcorrenciaStatusUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(write_permission),
):
    try:
        ocorrencia = ocorrencia_service.update_status(db, ocorrencia_id, payload.status)
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return OcorrenciaOut.model_validate(ocorrencia)


@router.delete("/{ocorrencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar(
    ocorrencia_id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(write_permission),
):
    try:
        ocorrencia_service.delete_ocorrencia(db, ocorrencia_id)
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{ocorrencia_id}/comments", response_model=List[ComentarioOut])
def listar_comentarios(
    ocorrencia_id: UUID,
    db: Session = Depends(get_db),
    _: None = Depends(read_permission),
):
    try:
        comentarios = ocorrencia_service.list_comments(db, ocorrencia_id)
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return [ComentarioOut.model_validate(item) for item in comentarios]


@router.post("/{ocorrencia_id}/comments", response_model=List[ComentarioOut])
def adicionar_comentarios(
    ocorrencia_id: UUID,
    payload: List[ComentarioCreate],
    db: Session = Depends(get_db),
    _: None = Depends(create_permission),
):
    try:
        comentarios = ocorrencia_service.add_comments(db, ocorrencia_id, payload)
    except OcorrenciaNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return [ComentarioOut.model_validate(item) for item in comentarios]
