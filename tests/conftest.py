import os

from dotenv import load_dotenv

# Precisa vir ANTES de importar qualquer coisa do src: o config.py lê DATABASE_URL
# na importação, e o load_dotenv não sobrescreve variáveis já definidas.
load_dotenv()
_test_url = os.environ["DATABASE_TEST_URL"].strip()
assert "zykgrpiloujecvfjikgp" not in _test_url, "DATABASE_TEST_URL aponta para PRODUÇÃO!"
os.environ["DATABASE_URL"] = _test_url

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import auth.service as auth_service
from config import DOMINIO_EMPRESA
from database.core import engine, get_db
from entities.users import Usuario
from main import app


def make_claims(**overrides):
    claims = {
        "sub": "google-123",
        "email": f"teste@{DOMINIO_EMPRESA}",
        "email_verified": True,
        "hd": DOMINIO_EMPRESA,
        "given_name": "Teste",
        "family_name": "Silva",
        "picture": "https://exemplo.com/foto.png",
    }
    return claims | overrides


@pytest.fixture(scope="session", autouse=True)
def migrar_banco():
    """Aplica as migrations uma vez por execução (cria btree_gist, constraints etc.)."""
    command.upgrade(Config("alembic.ini"), "head")


@pytest.fixture
def db_session():
    """Cada teste roda numa transação desfeita no final: o banco volta limpo."""
    conexao = engine.connect()
    transacao = conexao.begin()
    sessao = Session(bind=conexao, join_transaction_mode="create_savepoint")
    try:
        yield sessao
    finally:
        sessao.close()
        transacao.rollback()
        conexao.close()


@pytest.fixture
def google_claims(monkeypatch):
    """Substitui a verificação do Google. Os testes podem alterar o dict retornado."""
    claims = make_claims()
    monkeypatch.setattr(
        auth_service.id_token, "verify_oauth2_token", lambda token, req, aud: claims
    )
    return claims


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    user = Usuario(id_google="google-123", email=f"teste@{DOMINIO_EMPRESA}", nome="Teste")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    """Cabeçalho de usuário logado, para rotas protegidas sem passar pelo Google."""
    return {"Authorization": f"Bearer {auth_service.create_token(test_user)}"}
