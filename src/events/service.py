from sqlalchemy import func, select, type_coerce

from auth.service import CurrentUser
from sqlalchemy.dialects.postgresql import TSTZMULTIRANGE, TSTZRANGE, Range
from entities.eventos import Evento, Reserva
from .models import CreateEventSchema
from sqlalchemy.orm import Session, joinedload

from logs import logging

logger = logging.getLogger(__name__)

def create_event(event: CreateEventSchema, user: CurrentUser, db: Session) -> Evento:
    check_overlap(event, db)
    datas = [Range(inicio, fim, bounds="[)") for inicio, fim in event.datas]
    evento = Evento(
        nome=event.nome,
        criador_id=user,
        tipo=event.tipo,
        reservas=[Reserva(id_local=local_id, datas=datas) for local_id in event.locais],
    )
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return evento

def check_overlap(event: CreateEventSchema, db: Session) -> None:

    datas = [Range(start, end, bounds='[)') for start, end in event.datas]

    periodo_conflitante = type_coerce(
        func.unnest(Reserva.datas.intersection(type_coerce(datas, TSTZMULTIRANGE))),
        TSTZRANGE,
    )

    statement = (
        select(Reserva, periodo_conflitante)
        .options(joinedload(Reserva.local), joinedload(Reserva.evento))
        .where(Reserva.id_local.in_(event.locais),
               Reserva.datas.overlaps(datas)
        )
    )

    conflitos = db.execute(statement).all()

    if conflitos:
        linhas = [
            f"- {reserva.local.nome} (evento '{reserva.evento.nome}'): "
            f"{p.lower:%d/%m/%Y %H:%M} até {p.upper:%d/%m/%Y %H:%M}" # type: ignore
            for reserva, p in conflitos
        ]
        mensagem = "Conflito de datas:\n" + "\n".join(linhas)
        logger.warning(mensagem)
        raise ValueError(mensagem)
