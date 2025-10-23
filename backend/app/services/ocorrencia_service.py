from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple
from uuid import UUID

from sqlalchemy import asc, desc, func, or_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models.comentario import Comentario
from app.models.enums import PrioridadeEnum, StatusEnum
from app.models.ocorrencia import Ocorrencia
from app.schemas.comentario import ComentarioCreate


class OcorrenciaNotFoundError(NoResultFound):
    pass


def _parse_status(value: str) -> StatusEnum:
    try:
        return StatusEnum(value)
    except ValueError as exc:
        raise ValueError("Status inválido.") from exc


def _parse_prioridade(value: str) -> PrioridadeEnum:
    try:
        return PrioridadeEnum(value)
    except ValueError as exc:
        raise ValueError("Prioridade inválida.") from exc


def _apply_filters(query, status: Optional[str], prioridade: Optional[str], texto: Optional[str]):
    if status:
        query = query.filter(Ocorrencia.status == _parse_status(status))
    if prioridade:
        query = query.filter(Ocorrencia.prioridade == _parse_prioridade(prioridade))
    if texto:
        lowered = f"%{texto.lower()}%"
        query = query.filter(
            or_(
                func.lower(Ocorrencia.titulo).like(lowered),
                func.lower(Ocorrencia.descricao).like(lowered),
            )
        )
    return query


def list_ocorrencias(
    db: Session,
    *,
    page: int,
    size: int,
    status: Optional[str],
    prioridade: Optional[str],
    texto: Optional[str],
    sort_field: str,
    sort_direction: str,
) -> Tuple[Sequence[Ocorrencia], int]:
    query = db.query(Ocorrencia)
    query = _apply_filters(query, status, prioridade, texto)

    total = query.count()

    sort_attr = {
        "dataAbertura": Ocorrencia.data_abertura,
        "dataAtualizacao": Ocorrencia.data_atualizacao,
        "titulo": Ocorrencia.titulo,
        "prioridade": Ocorrencia.prioridade,
        "status": Ocorrencia.status,
    }.get(sort_field, Ocorrencia.data_abertura)

    direction = desc if sort_direction.lower() == "desc" else asc
    query = query.order_by(direction(sort_attr))

    offset = page * size
    items = query.offset(offset).limit(size).all()
    return items, total


def get_ocorrencia(db: Session, ocorrencia_id: UUID) -> Ocorrencia:
    ocorrencia = db.query(Ocorrencia).filter_by(id=ocorrencia_id).first()
    if not ocorrencia:
        raise OcorrenciaNotFoundError("Ocorrência não encontrada")
    return ocorrencia


def create_ocorrencia(db: Session, payload: dict) -> Ocorrencia:
    payload = payload.copy()
    payload["prioridade"] = _parse_prioridade(payload["prioridade"])
    payload["status"] = _parse_status(payload["status"])

    ocorrencia = Ocorrencia(**payload)
    db.add(ocorrencia)
    db.flush()
    return ocorrencia


def update_ocorrencia(db: Session, ocorrencia_id: UUID, payload: dict) -> Ocorrencia:
    ocorrencia = get_ocorrencia(db, ocorrencia_id)
    updates = payload.copy()
    if "prioridade" in updates:
        updates["prioridade"] = _parse_prioridade(updates["prioridade"])
    if "status" in updates:
        updates["status"] = _parse_status(updates["status"])

    for field, value in updates.items():
        setattr(ocorrencia, field, value)
    db.flush()
    return ocorrencia


def delete_ocorrencia(db: Session, ocorrencia_id: UUID) -> None:
    ocorrencia = get_ocorrencia(db, ocorrencia_id)
    db.delete(ocorrencia)


def update_status(db: Session, ocorrencia_id: UUID, status_code: str) -> Ocorrencia:
    ocorrencia = get_ocorrencia(db, ocorrencia_id)
    ocorrencia.status = _parse_status(status_code)
    db.flush()
    return ocorrencia


def list_comments(db: Session, ocorrencia_id: UUID) -> List[Comentario]:
    get_ocorrencia(db, ocorrencia_id)
    return (
        db.query(Comentario)
        .filter(Comentario.ocorrencia_id == ocorrencia_id)
        .order_by(Comentario.data_criacao.desc())
        .all()
    )


def add_comments(
    db: Session,
    ocorrencia_id: UUID,
    comentarios: Iterable[ComentarioCreate],
) -> List[Comentario]:
    ocorrencia = get_ocorrencia(db, ocorrencia_id)
    saved: List[Comentario] = []
    for comentario_data in comentarios:
        entity = Comentario(
            ocorrencia_id=ocorrencia.id,
            autor=comentario_data.autor,
            mensagem=comentario_data.mensagem,
        )
        db.add(entity)
        saved.append(entity)
    db.flush()
    return saved


def get_estatisticas(db: Session):
    total = db.query(func.count(Ocorrencia.id)).scalar() or 0

    status_rows = (
        db.query(Ocorrencia.status.label("chave"), func.count(Ocorrencia.id).label("valor"))
        .group_by(Ocorrencia.status)
        .all()
    )

    prioridade_rows = (
        db.query(Ocorrencia.prioridade.label("chave"), func.count(Ocorrencia.id).label("valor"))
        .group_by(Ocorrencia.prioridade)
        .all()
    )

    def _convert(rows):
        return [
            {
                "chave": row.chave.value if isinstance(row.chave, (StatusEnum, PrioridadeEnum)) else row.chave,
                "valor": int(row.valor),
            }
            for row in rows
        ]

    return {
        "total": int(total),
        "status": _convert(status_rows),
        "prioridade": _convert(prioridade_rows),
    }
