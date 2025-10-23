from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from app.models.enums import PrioridadeEnum, StatusEnum


class OcorrenciaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    prioridade: str
    status: str
    email_responsavel: str = Field(alias="emailResponsavel")
    tags: Optional[List[str]] = None

    model_config = ConfigDict(populate_by_name=True)


class OcorrenciaCreate(OcorrenciaBase):
    pass


class OcorrenciaUpdate(OcorrenciaBase):
    pass


class OcorrenciaStatusUpdate(BaseModel):
    status: str


class OcorrenciaOut(BaseModel):
    id: UUID
    titulo: str
    descricao: Optional[str]
    prioridade: PrioridadeEnum
    status: StatusEnum
    email_responsavel: str = Field(alias="emailResponsavel")
    tags: Optional[List[str]]
    data_abertura: datetime = Field(alias="dataAbertura")
    data_atualizacao: datetime = Field(alias="dataAtualizacao")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_serializer("prioridade")
    def serialize_prioridade(self, value: PrioridadeEnum) -> Optional[dict[str, str]]:
        if value is None:
            return None
        return {"code": value.value, "label": value.label}

    @field_serializer("status")
    def serialize_status(self, value: StatusEnum) -> Optional[dict[str, str]]:
        if value is None:
            return None
        return {"code": value.value, "label": value.label}
