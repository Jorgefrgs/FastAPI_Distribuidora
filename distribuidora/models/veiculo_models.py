from pydantic import BaseModel
from typing import Optional

class VeiculoRequest(BaseModel):
    marca: str
    modelo: str
    ano: int
    status_ativo: Optional[bool] = True


class VeiculoResponse(BaseModel):
    id: int
    motorista_id: int
    marca: str
    modelo: str
    ano: int

    class Config:
        orm_mode = True