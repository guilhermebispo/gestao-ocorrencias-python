from __future__ import annotations

from typing import List, Optional
from uuid import UUID
from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.db import Base
from app.models.enums import PrioridadeEnum, StatusEnum


class Ocorrencia(Base):
    __tablename__ = "tb_ocorrencia"

    id: UUID = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    titulo: str = Column(String(120), nullable=False)
    descricao: Optional[str] = Column(Text, nullable=True)
    prioridade: PrioridadeEnum = Column(
        Enum(PrioridadeEnum, name="prioridade_enum", native_enum=False, create_constraint=False),
        nullable=False,
    )
    status: StatusEnum = Column(
        Enum(StatusEnum, name="status_enum", native_enum=False, create_constraint=False),
        nullable=False,
    )
    email_responsavel: str = Column(String(255), nullable=False)

    tags: Optional[List[str]] = Column(PG_ARRAY(String, dimensions=1), nullable=True)

    data_abertura = Column(DateTime, nullable=False, server_default=func.now())
    data_atualizacao = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def atualizar(self, other: "Ocorrencia") -> None:
        self.titulo = other.titulo
        self.descricao = other.descricao
        self.prioridade = other.prioridade
        self.status = other.status
        self.email_responsavel = other.email_responsavel
        self.tags = other.tags
