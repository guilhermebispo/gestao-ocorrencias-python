from __future__ import annotations

from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, relationship

from app.db import Base


class Comentario(Base):
    __tablename__ = "tb_comentario"

    id: UUID = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    ocorrencia_id: UUID = Column(PG_UUID(as_uuid=True), ForeignKey("tb_ocorrencia.id", ondelete="CASCADE"), nullable=False)
    autor: str = Column(String(120), nullable=False)
    mensagem: str = Column(Text, nullable=False)
    data_criacao = Column(DateTime, nullable=False, server_default=func.now())

    ocorrencia: Mapped["Ocorrencia"] = relationship("Ocorrencia", backref="comentarios")

    @property
    def id_ocorrencia(self) -> UUID:
        return self.ocorrencia_id
