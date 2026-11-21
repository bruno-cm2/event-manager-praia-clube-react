import logging
from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.auth.transport import requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from auth.models import GoogleLogin, GoogleSignup, GoogleUserInfo
from config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    DOMINIO_EMPRESA,
    GOOGLE_CLIENT_ID,
    SECRET_KEY,
)
from database.core import SessionDep
from entities import Usuario
from entities.users import Departamento

logger = logging.getLogger(__name__)


bearer = HTTPBearer()


def verify_google_token(token: str) -> GoogleUserInfo:
    try:
        claims = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID
        )
    except ValueError:
        logger.error("Token do Google inválido.")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Token do Google inválido."
        )

    info = GoogleUserInfo.model_validate(claims)
    if info.hd != DOMINIO_EMPRESA or not info.email_verified:
        logger.warning("Login recusado fora do domínio: %s", info.email)
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Acesso restrito a contas da empresa",
        )
    return info


def authenticate_user(login: GoogleLogin, db: Session) -> Usuario:
    info = verify_google_token(login.id_google)
    user = db.query(Usuario).filter(Usuario.id_google == info.sub).first()
    if not user:
        logger.info(f"Usuário {info.email} não encontrado. Criando novo usuário.")
        user = create_user(info, db)
    if not user.ativo:
        logger.warning(f"Usuário {user.email} tentou logar, mas está inativo.")
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Esta conta foi desativada."
        )
    user.email, user.nome, user.sobrenome, user.foto_url = (
        info.email,
        info.nome,
        info.family_name,
        info.picture,
    )
    db.commit()
    return user


def create_user(info: GoogleUserInfo, db: Session) -> Usuario:
    user = Usuario(
        id_google=info.sub,
        email=info.email,
        nome=info.nome,
        sobrenome=info.family_name,
        foto_url=info.picture,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Novo usuário {user.email} criado com sucesso.")
    return user


def complete_signup(user: Usuario, dados: GoogleSignup, db: Session) -> Usuario:
    if dados.id_departamento is not None and not db.get(
        Departamento, dados.id_departamento
    ):
        raise HTTPException(404, "Departamento não encontrado.")
    user.id_departamento = dados.id_departamento
    user.area = dados.area
    db.commit()
    db.refresh(user)
    return user


def create_token(user: Usuario) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user.id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
    )


def get_current_user(
    db: SessionDep,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
) -> Usuario:
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        logger.warning("Token inválido ou expirado.")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Token inválido ou expirado."
        )

    user = db.get(Usuario, user_id)
    if not user or not user.ativo:
        logger.warning(f"Usuário com ID {user_id} não encontrado ou inativo.")
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo.",
        )
    return user


CurrentUser = Annotated[Usuario, Depends(get_current_user)]


def get_admin(user: CurrentUser) -> Usuario:
    if not user.admin:
        logger.warning(
            f"Usuário {user.email} tentou acessar rota de admin sem permissão."
        )
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Acesso restrito a administradores.",
        )
    return user


Admin = Annotated[CurrentUser, Depends(get_admin)]
