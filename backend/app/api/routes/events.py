import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Event, EventBase, EventCreate, EventUpdate, EventsPublic

router = APIRouter()


@router.get("/", response_model=EventsPublic) 
def read_events(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve events.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Event)
        count = session.exec(count_statement).one()
        statement = select(Event).offset(skip).limit(limit)
        events = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Event)
            .where(Event.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Event)
            .where(Event.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        events = session.exec(statement).all()

    return EventsPublic(data=events, count=count)

@router.post("/", response_model=EventCreate)
def create_event(
    *, session: SessionDep, current_user: CurrentUser, event_in: EventCreate
) -> Any:
    """
    Create new event.
    """
    event = Event.model_validate(event_in, update={"owner_id": current_user.id})
    session.add(event)
    session.commit()
    session.refresh(event)
    return event