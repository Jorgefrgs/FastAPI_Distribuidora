from pydantic import BaseModel
from typing import Optional

class FornecedorRequest(BaseModel):
    nome: str
    endereco: str
    email: str
    telefone: str
    cnpj: str


class FornecedorResponse(BaseModel):
    id: int
    nome: str
    endereco: str
    email: str
    telefone: str
    cnpj: str
    status_ativo: bool

    class Config:
        orm_mode = True
