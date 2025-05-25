from pydantic import BaseModel

class FilmeBase(BaseModel):
    titulo: str
    diretor: str
    ano: int

class FilmeCreate(FilmeBase):
    pass

class Filme(FilmeBase):
    id: int

    class Config:
        orm_mode = True
