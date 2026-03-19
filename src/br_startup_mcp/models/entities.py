"""Pydantic v2 models for br-startup-mcp entities."""

import hashlib
from datetime import date, datetime
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


class Startup(BaseModel):
    """Dados cadastrais de startup da Receita Federal (via BrasilAPI)."""

    model_config = {"from_attributes": True}

    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    situacao_cadastral: str
    data_abertura: date
    capital_social_brl: float
    cnae_principal: str
    cnaes_secundarios: list[str] = []
    natureza_juridica: str
    porte: str
    endereco_logradouro: Optional[str] = None
    cidade: str
    estado: str
    cep: Optional[str] = None
    updated_at: datetime


class Founder(BaseModel):
    """Sócio/fundador derivado do quadro societário da Receita Federal."""

    model_config = {"from_attributes": True}

    id: str
    cnpj_empresa: str
    nome: str
    cpf_cnpj: Optional[str] = None
    qualificacao: str
    participacao_pct: Optional[float] = None
    data_entrada: Optional[date] = None
