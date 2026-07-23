from typing import Optional

from pydantic import BaseModel, HttpUrl

class ArtigoSchema(BaseModel):
    id: Optional[int]
    titulo: str
    descricao: str
    url_fonte: HttpUrl
    usuario_id: int