from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuario_model import UsuarioModel


class TokenData(BaseModel):

    username: Optional[str] = None


async def get_session() -> Generator:
    """
    Gera uma sessão assíncrona do banco de dados.

    Yields:
        AsyncSession: Sessão assíncrona do banco de dados.
    """

    session: AsyncSession = Session()

    async with Session() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_schema),
) -> UsuarioModel:
    """
    Obtém o usuário atual com base no token JWT fornecido.

    Args:
        token (str): O token JWT fornecido pelo usuário.
        db (AsyncSession): Sessão assíncrona do banco de dados.

    Returns:
        UsuarioModel: O modelo do usuário autenticado.

    Raises:
        HTTPException: Se o token for inválido ou se o usuário não for encontrado.
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data: TokenData = TokenData(username=username)

    except JWTError:
        raise credential_exception

    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == token_data.username)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if usuario is None:
            raise credential_exception

        return usuario
