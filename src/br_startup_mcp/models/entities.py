"""Pydantic v2 models for br-startup-mcp entities."""

import hashlib
from datetime import date
from typing import Optional

from pydantic import BaseModel


def make_id(*parts: str) -> str:
    """Generate a short stable ID from parts."""
    return hashlib.md5("_".join(parts).encode()).hexdigest()[:12]


class BndesOperation(BaseModel):
    """Represents a financing operation contracted with BNDES."""

    model_config = {"from_attributes": True}

    id: str
    cnpj_cliente: str
    razao_social: str
    produto_bndes: str
    valor_brl: float
    data_contratacao: date
    setor_bndes: Optional[str] = None
    porte: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None


class CvmOffer(BaseModel):
    """Represents an equity crowdfunding offer (CVM Resolution 88/2022)."""

    model_config = {"from_attributes": True}

    id: str
    cnpj_emissora: str
    razao_social: str
    plataforma: str
    valor_alvo_brl: float
    valor_captado_brl: Optional[float] = None
    data_registro: date
    data_encerramento: Optional[date] = None
    status: str
    tipo_valor_mobiliario: Optional[str] = None
