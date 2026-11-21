from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TSTZMULTIRANGE, ExcludeConstraint, Range
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    criador_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    criador: Mapped["Usuario"] = relationship(back_populates="eventos")  # type: ignore
    reservas: Mapped[list["Reserva"]] = relationship(
        back_populates="evento", cascade="all, delete-orphan"
    )


class Reserva(Base):
    __tablename__ = "reservas"

    id_evento: Mapped[int] = mapped_column(ForeignKey("eventos.id"), primary_key=True)
    id_local: Mapped[int] = mapped_column(ForeignKey("locais.id"), primary_key=True)
    evento: Mapped["Evento"] = relationship(back_populates="reservas")
    local: Mapped["Local"] = relationship(back_populates="reservas")  # type: ignore
    datas: Mapped[list[Range[datetime]]] = mapped_column(TSTZMULTIRANGE, nullable=False)

    __table_args__ = (
        ExcludeConstraint(
            ("id_local", "="),
            ("datas", "&&"),
            name="reserva_overlap",
            using="gist",
        ),
    )
