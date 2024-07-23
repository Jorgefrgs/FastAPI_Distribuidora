from pydantic import BaseModel, conint
from typing import Optional

class VeiculoRequest(BaseModel):
    marca: str
    modelo: str
    placa: str
    ano: conint(ge=1900, le=2024)
    motorista_id: conint(ge=1)
    status_ativo: Optional[bool] = True


class VeiculoResponse(BaseModel):
    id: int
    motorista_id: int
    marca: str
    modelo: str
    ano: int

    class Config:
        orm_mode = True