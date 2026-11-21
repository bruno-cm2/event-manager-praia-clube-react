from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, false, func, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_google: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    sobrenome: Mapped[str | None]
    foto_url: Mapped[str | None]
    id_departamento: Mapped[int | None] = mapped_column(ForeignKey("departamentos.id"))
    departamento: Mapped["Departamento | None"] = relationship(
        back_populates="usuarios"
    )
    area: Mapped[str | None]
    admin: Mapped[bool] = mapped_column(default=False, server_default=false())
    ativo: Mapped[bool] = mapped_column(default=True, server_default=true())
    eventos: Mapped[list["Evento"]] = relationship(back_populates="criador")  # type: ignore
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Departamento(Base):
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="departamento")
