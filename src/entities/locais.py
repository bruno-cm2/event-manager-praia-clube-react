from database.core import Base
from sqlalchemy import ForeignKey, true
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Setor(Base):
    __tablename__ = "setores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    locais: Mapped[list["Local"]] = relationship(back_populates="setor")
    ativo: Mapped[bool] = mapped_column(default=True, server_default=true())

class Local(Base):
    __tablename__ = "locais"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_setor: Mapped[int] = mapped_column(ForeignKey("setores.id"), nullable=False)
    setor: Mapped["Setor"] = relationship(back_populates="locais")
    nome: Mapped[str] = mapped_column(nullable=False)
    ativo: Mapped[bool] = mapped_column(default=True, server_default=true())
    reservas: Mapped[list["Reserva"]] = relationship(back_populates="local", cascade="all, delete-orphan") # type: ignore