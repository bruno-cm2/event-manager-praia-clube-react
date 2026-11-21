from datetime import datetime

from pydantic import BaseModel

class CreateEventSchema(BaseModel):
    nome: str
    locais: list[int]
    datas: list[tuple[datetime, datetime]]
    tipo: str