from app.schemas.auth import Credenciais
from app.schemas.comentario import ComentarioCreate, ComentarioOut
from app.schemas.common import ApiError, ApiErrorDetail, Dominio, PageResponse
from app.schemas.ocorrencia import (
    OcorrenciaCreate,
    OcorrenciaOut,
    OcorrenciaStatusUpdate,
    OcorrenciaUpdate,
)
from app.schemas.stats import Estatistica, Resultado
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioOut,
    UsuarioPerfilUpdate,
    UsuarioSenhaUpdate,
    UsuarioUpdate,
)

__all__ = [
    "ApiError",
    "ApiErrorDetail",
    "Dominio",
    "PageResponse",
    "ComentarioCreate",
    "ComentarioOut",
    "OcorrenciaCreate",
    "OcorrenciaOut",
    "OcorrenciaStatusUpdate",
    "OcorrenciaUpdate",
    "Estatistica",
    "Resultado",
    "UsuarioCreate",
    "UsuarioOut",
    "UsuarioPerfilUpdate",
    "UsuarioSenhaUpdate",
    "UsuarioUpdate",
    "Credenciais",
]
