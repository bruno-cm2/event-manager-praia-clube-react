from http import HTTPStatus

from entities.users import Usuario


def test_login_cria_usuario_novo(client, db_session, google_claims):
    resp = client.post("/auth/google", json={"id_google": "token-falso"})

    assert resp.status_code == HTTPStatus.OK
    body = resp.json()
    assert body["access_token"]
    assert body["usuario"]["email"] == google_claims["email"]
    assert db_session.query(Usuario).filter_by(id_google="google-123").count() == 1


def test_login_usuario_existente_atualiza_dados(client, test_user, google_claims):
    google_claims["given_name"] = "Novo Nome"

    resp = client.post("/auth/google", json={"id_google": "token-falso"})

    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["usuario"]["id"] == test_user.id
    assert resp.json()["usuario"]["nome"] == "Novo Nome"


def test_login_fora_do_dominio(client, google_claims):
    google_claims.update(hd="gmail.com", email="alguem@gmail.com")

    resp = client.post("/auth/google", json={"id_google": "token-falso"})

    assert resp.status_code == HTTPStatus.FORBIDDEN


def test_login_email_nao_verificado(client, google_claims):
    google_claims["email_verified"] = False

    resp = client.post("/auth/google", json={"id_google": "token-falso"})

    assert resp.status_code == HTTPStatus.FORBIDDEN


def test_token_google_invalido(client, monkeypatch):
    from auth import service

    def falha(*args):
        raise ValueError("token inválido")

    monkeypatch.setattr(service.id_token, "verify_oauth2_token", falha)

    resp = client.post("/auth/google", json={"id_google": "lixo"})

    assert resp.status_code == HTTPStatus.UNAUTHORIZED


def test_usuario_inativo(client, db_session, test_user, google_claims):
    test_user.ativo = False
    db_session.commit()

    resp = client.post("/auth/google", json={"id_google": "token-falso"})

    assert resp.status_code == HTTPStatus.FORBIDDEN


def test_me_com_token(client, auth_headers, test_user):
    resp = client.get("/auth/me", headers=auth_headers)

    assert resp.status_code == HTTPStatus.OK
    assert resp.json()["id"] == test_user.id


def test_me_sem_token(client):
    assert client.get("/auth/me").status_code == HTTPStatus.UNAUTHORIZED