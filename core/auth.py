from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.usuario_model import UsuarioModel
from core.configs import settings
from core.security import verificar_senha
from pydantic import (
    EmailStr,
)  # Pydantic já tem validação de e-mail, então podemos usar o EmailStr para validar o e-mail do usuário

# Permite que criemos um endpoint para autenticação
oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/usuarios/login")


async def autenticar(
    email: EmailStr, senha: str, db: AsyncSession
) -> Optional[UsuarioModel]:
    """
    Autentica um usuário com base no e-mail e senha fornecidos.

    Args:
        email (EmailStr): O e-mail do usuário.
        senha (str): A senha fornecida pelo usuário.
        db (AsyncSession): Sessão assíncrona do banco de dados.

    Returns:
        Optional[UsuarioModel]: O modelo do usuário autenticado, ou None se a autenticação falhar.
    """
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().first()

        if not usuario:
            return None

        if not verificar_senha(senha, usuario.senha):
            return None

        return usuario


def criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    """
    Cria um token JWT com base no tipo, tempo de vida e assunto fornecidos.

    Args:
        tipo_token (str): O tipo do token (ex: "access" ou "refresh").
        tempo_vida (timedelta): O tempo de vida do token.
        sub (str): O assunto do token (geralmente o ID do usuário).
    """

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # Dê uma olhada no site acima depois, pois ele explica o que é o payload do JWT e como ele funciona.
    # Explica especificações json web token, que é o que estamos usando aqui.

    payload = {}
    sp = timezone("America/Sao_Paulo")
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token  # Tipo do token (access ou refresh)
    payload["exp"] = expira  # Data e hora de expiração do token
    payload["iat"] = datetime.now(tz=sp)  # Data e hora de emissão (issued at) do token
    payload["sub"] = str(
        sub
    )  # Subject - identificador único do usuário (geralmente o ID)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def criar_token_acesso(sub: str) -> str:

    # Dá uma olhada nesse site depois, pois ele explica o que é o JWT e como ele funciona.
    """
    https://jwt.io/introduction/
    """

    return criar_token(
        tipo_token="access_token",
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )
