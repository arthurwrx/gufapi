from typing import Optional
from typing import List

from pydantic import BaseModel, EmailStr

from schemas.artigo_schema import ArtigoSchema

class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    eh_admin: bool = False
    
    class Config:
        orm_mode = True
        

class UsuarioSchemaCreate(UsuarioSchemaBase): # UsuarioSchemaCreate herda de UsuarioSchemaBase, então ele já tem todos os campos de UsuarioSchemaBase, e adiciona o campo senha
    senha: str
    
    
class UsuarioSchemaArtigos(UsuarioSchemaBase): # UsuarioSchemaArtigos herda de UsuarioSchemaBase, então ele já tem todos os campos de UsuarioSchemaBase, e adiciona o campo artigos
    artigos: List[ArtigoSchema] = []
    
class UsuarioSchemaUp(UsuarioSchemaBase): # UsuarioSchemaUp herda de UsuarioSchemaBase, então ele já tem todos os campos de UsuarioSchemaBase, e adiciona o campo senha
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    eh_admin: Optional[bool] = None