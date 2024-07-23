from pydantic import BaseModel, constr
class FornecedorRequest(BaseModel):
    nome: str
    endereco: str
    email: str
    telefone: str
    cnpj: constr(min_length=14, max_length=14)

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
