from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Resultado(BaseModel):
    chave: str
    valor: int


class Estatistica(BaseModel):
    total: int
    status: List[Resultado]
    prioridade: List[Resultado]
