from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ComentarioCreate(BaseModel):
    autor: str
    mensagem: str


class ComentarioOut(BaseModel):
    id: UUID
    id_ocorrencia: UUID = Field(alias="idOcorrencia")
    autor: str
    mensagem: str
    data_criacao: datetime = Field(alias="dataCriacao")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
