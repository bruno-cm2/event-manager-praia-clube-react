from . import service
from fastapi import APIRouter
from .models import GoogleLogin, GoogleSignup, Token, UserResponse

from database.core import SessionDep

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/google", response_model=Token)
def google_login(body: GoogleLogin, db: SessionDep):
    user = service.authenticate_user(body, db)
    access_token = service.create_token(user)
    return Token(access_token=access_token, usuario=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
def me(user: service.CurrentUser):
    return user


@router.patch("/me", response_model=UserResponse)
def completar_cadastro(body: GoogleSignup, user: service.CurrentUser, db: SessionDep):
    return service.complete_signup(user, body, db)
