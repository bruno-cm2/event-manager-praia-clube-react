from pydantic import BaseModel, ConfigDict


class GoogleLogin(BaseModel):
    id_google: str


class GoogleSignup(BaseModel):
    id_departamento: int | None
    area: str | None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    nome: str
    sobrenome: str | None
    foto_url: str | None
    id_departamento: int | None
    area: str | None
    admin: bool


class GoogleUserInfo(BaseModel):
    sub: str
    email: str
    email_verified: bool = False
    hd: str | None = None  # domínio do Workspace
    name: str | None = None
    given_name: str | None = None
    family_name: str | None = None
    picture: str | None = None

    @property
    def nome(self) -> str:
        return self.given_name or self.name or self.email


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UserResponse
