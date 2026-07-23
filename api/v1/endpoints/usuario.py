from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaArtigos, UsuarioSchemaUp
from core.deps import get_session, get_current_user
from core.security import verificar_hash_senha, gerar_hash_senha
from core.auth import autenticar, criar_token_acesso

router = APIRouter()

# GET LOGADO
@router.get("/logado", response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario_logado(
    usuario_logado: UsuarioModel = Depends(get_current_user)
):
    return usuario_logado

# POST / Sign up
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(
    usuario: UsuarioSchemaCreate,
    db: AsyncSession = Depends(get_session)
):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        eh_admin=usuario.eh_admin
    )

    async with db as session:
        session.add(novo_usuario)
        await session.commit()

        
        return novo_usuario
    
# GET Usuarios
@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuarios(
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioModel] = result.scalars().unique().all()
        
        return usuarios
    
# GET Usuario
@router.get("/{usuario_id}", response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        
        return usuario
    
# PUT USUARIO
@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(
    usuario_id: int,
    usuario: UsuarioSchemaUp,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        
        if not usuario_up:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        if usuario.nome:
            usuario_up.nome = usuario.nome
        if usuario.sobrenome:
            usuario_up.sobrenome = usuario.sobrenome
        if usuario.email:
            usuario_up.email = usuario.email
        if usuario.senha:
            usuario_up.senha = gerar_hash_senha(usuario.senha)
            
        await session.commit()

        return usuario_up
    
# DELETE USUARIO
@router.delete("/{usuario_id}", response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def delete_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(UsuarioModel).where(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_del: UsuarioModel = result.scalars().unique().one_or_none()
        
        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()
            return usuario_del
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
    
# POST LOGIN
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    usuario = await autenticar(form_data.username, form_data.password, db)

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )


    return JSONResponse(content={"access_token": criar_token_acesso(sub=usuario.email), "token_type": "bearer"}, status_code=status.HTTP_200_OK)