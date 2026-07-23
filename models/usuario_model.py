from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings


class UsuarioModel(settings.DBBaseModel):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(
        String(256), nullable=True
    )  # nullable significa que basta ele informar o email e a senha, o nome não é obrigatório
    sobrenome = Column(String(256), nullable=True)
    email = Column(String(256), unique=True, index=True, nullable=False)
    senha = Column(String(256), nullable=False)
    artigos = relationship(
        "ArtigoModel",
        back_populates="criador",
        lazy="joined",
        cascade="all, delete-orphan",
        uselist=True,
    )  # lazy="joined" significa que quando eu buscar um usuário, ele já vai trazer os artigos dele junto, e cascade="all, delete-orphan" significa que quando eu deletar um usuário, ele vai deletar todos os artigos dele também
