from __future__ import annotations

from enum import Enum


class StatusEnum(str, Enum):
    ABERTA = "ABERTA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    RESOLVIDA = "RESOLVIDA"
    CANCELADA = "CANCELADA"

    @property
    def label(self) -> str:
        return {
            StatusEnum.ABERTA: "Aberta",
            StatusEnum.EM_ANDAMENTO: "Em andamento",
            StatusEnum.RESOLVIDA: "Resolvida",
            StatusEnum.CANCELADA: "Cancelada",
        }[self]


class PrioridadeEnum(str, Enum):
    BAIXA = "BAIXA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

    @property
    def label(self) -> str:
        return {
            PrioridadeEnum.BAIXA: "Baixa",
            PrioridadeEnum.MEDIA: "Média",
            PrioridadeEnum.ALTA: "Alta",
        }[self]


class PerfilEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

    @property
    def label(self) -> str:
        return {
            PerfilEnum.ADMIN: "Administrador",
            PerfilEnum.USER: "Usuário",
        }[self]
