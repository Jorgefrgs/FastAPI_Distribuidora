from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from distribuidora.models.veiculo_models import VeiculoRequest, VeiculoResponse

class EncomendaRequest(BaseModel):
    cliente: str
    quantidade: int
    descricao: str
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

    class Config:
        orm_mode = True

class ClienteRequest(BaseModel):
    nome: str
    idade: int
    endereco: str
    telefone: str
    cpf: str

class ClienteResponse(BaseModel):
    id: int
    nome: str
    idade: int
    endereco: str
    telefone: str
    status_atividade: bool
    cpf: str
    data_registro: datetime

    class Config:
        orm_mode = True

class MotoristaRequest(BaseModel):
    nome: str
    idade: int
    telefone: str
    endereco: str
    email: str
    cpf: str
    veiculo: Optional[VeiculoRequest] = None


class MotoristaResponse(BaseModel):
    id: int
    idade: int
    nome: str
    telefone: str
    endereco: str
    email: str
    status_ativo: bool
    cpf: str
    veiculo: Optional[VeiculoResponse] = None


    class Config:
        orm_mode = True


