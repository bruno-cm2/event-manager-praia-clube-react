from datetime import datetime

from database.core import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func, true, false



class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(nullable=False)
    nome: Mapped[str] = mapped_column(nullable=False)
    sobrenome: Mapped[str]
    id_departamento: Mapped[int] = mapped_column(ForeignKey("departamentos.id"), nullable=False)
    departamento: Mapped["Departamento"] = relationship(back_populates="usuarios")
    area: Mapped[str] = mapped_column(nullable=False)
    admin: Mapped[bool] = mapped_column(default=False, server_default=false())
    ativo: Mapped[bool] = mapped_column(default=True, server_default=true())
    eventos: Mapped[list["Evento"]] = relationship(back_populates="criador") # type: ignore
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Departamento(Base):
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="departamento")
