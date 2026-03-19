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
    """Dados cadastrais de startup da Receita Federal (via BrasilAPI), enriquecidos com Crunchbase."""

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
    # Crunchbase enrichment fields (optional — populated via enrich_startup_with_crunchbase)
    crunchbase_uuid: Optional[str] = None
    crunchbase_slug: Optional[str] = None
    categorias: list[str] = []
    descricao: Optional[str] = None
    website: Optional[str] = None
    total_funding_usd: Optional[float] = None
    last_funding_type: Optional[str] = None
    last_funding_date: Optional[date] = None
    employee_count: Optional[str] = None


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


class Round(BaseModel):
    """Represents a funding round for a startup. Source: Crunchbase API."""

    model_config = {"from_attributes": True}

    id: str
    cnpj_empresa: Optional[str] = None
    crunchbase_org_uuid: str
    company_name: str
    round_type: str
    announced_date: Optional[date] = None
    amount_usd: Optional[float] = None
    pre_money_valuation_usd: Optional[float] = None
    post_money_valuation_usd: Optional[float] = None
    lead_investor_name: Optional[str] = None
    investors: list[str] = []
    is_equity: Optional[bool] = None


class Investor(BaseModel):
    """Represents a VC fund, angel investor, CVC or accelerator. Source: Crunchbase API."""

    model_config = {"from_attributes": True}

    id: str
    crunchbase_uuid: str
    name: str
    type: str
    country: Optional[str] = None
    city: Optional[str] = None
    cnpj_fundo: Optional[str] = None
    cvm_patrimonio_brl: Optional[float] = None
    cvm_administrador: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
