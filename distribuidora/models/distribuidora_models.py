from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, conint, constr

from distribuidora.models.fornecedor_models import FornecedorResponse


class EncomendaRequest(BaseModel):
    cliente: str
    quantidade: int
    descricao: str
    produtos: List[int]
    status_encomenda: Optional[bool] = True

class EncomendaResponse(BaseModel):
    id: int
    cliente_id: int
    quantidade: int
    descricao: str
    prazo_entrega: datetime
    data_pedido: datetime
    status_encomenda: bool
    motorista_id: int
    veiculo_id: int
    fornecedor: Optional[FornecedorResponse] = None
    produtos: List[int]

    class Config:
        orm_mode = True

class ClienteRequest(BaseModel):
    nome: str
    idade: conint(ge=0)
    endereco: str
    telefone: str
    email: str
    cpf: constr(min_length=11, max_length=11)

class ClienteResponse(BaseModel):
    id: int
    nome: str
    idade: int
    endereco: str
    telefone: str
    email: str
    status_atividade: bool
    cpf: str
    data_registro: datetime

    class Config:
        orm_mode = True

class MotoristaRequest(BaseModel):
    nome: str
    idade: conint(ge=0)
    telefone: str
    endereco: str
    email: str
    cpf: constr(min_length=11, max_length=11)

class MotoristaResponse(BaseModel):
    id: int
    idade: int
    nome: str
    telefone: str
    endereco: str
    email: str
    status_ativo: bool
    cpf: str

    class Config:
        orm_mode = True

class PagamentoRequest(BaseModel):
    encomenda_id: int
    valor: conint(ge=0)
    metodo_pagamento: str

class PagamentoResponse(BaseModel):
    id: int
    encomenda_id: int
    valor: int
    data_pagamento: datetime
    metodo_pagamento: str

    class Config:
        orm_mode = True

class ProdutoRequest(BaseModel):
    nome: str
    descricao: str
    preco: conint(ge=0)
    categoria_id: int
    fornecedor_id: int

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: int
    categoria_id: int
    fornecedor_id: int
    data_criacao: datetime

    class Config:
        orm_mode = True

class CategoriaRequest(BaseModel):
    nome: str
    descricao: str

class CategoriaResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    data_criacao: datetime

    class Config:
        orm_mode = True
