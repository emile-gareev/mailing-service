from fastapi import Depends, Response, status
from fastapi_filter import FilterDepends
from fastapi.routing import APIRouter

from app.constants import DEFAULT_FROM_EMAIL
from app.dependencies.security import get_current_user
from app.dependencies.services import get_sent_email_service
from app.errors.base import NotFoundError
from app.errors.custom_exception import NotFoundException
from app.repositories.security import ServiceUserSchema
from app.routers.error_shema import ErrorMessage
from app.routers.internal.v1.filters import SentEmailFilter
from app.routers.internal.v1.schemas import (
    CounterSchema,
    SentEmailInputSchema,
    SentEmailSchema,
    SentEmailsListSchema,
)
from app.services.sent_email_service import SentEmailService

router = APIRouter()


@router.get(
    '/',
    response_model=SentEmailsListSchema,
    responses={
        200: {'model': SentEmailsListSchema, 'description': 'List of all sent emails'},
    },
)
async def list_sent_emails(
    page: int = 1,
    limit: int = 30,
    user: ServiceUserSchema = Depends(get_current_user),
    filtering: SentEmailFilter = FilterDepends(SentEmailFilter),
    service: SentEmailService = Depends(get_sent_email_service),
):
    """Get a list of all sent emails."""
    total_count = await service.get_sent_emails_count(filtering=filtering)
    sent_emails = await service.list_sent_emails(page, limit=limit, filtering=filtering)
    return {'count': total_count, 'results': sent_emails}


@router.post(
    '/',
    responses={201: {'model': SentEmailSchema, 'description': 'Creating a record of a sent email'}},
)
async def create_sent_email(
    input_data: SentEmailInputSchema,
    response: Response,
    user: ServiceUserSchema = Depends(get_current_user),
    service: SentEmailService = Depends(get_sent_email_service),
):
    """Creating a record in the database about the sent email."""
    response.status_code = status.HTTP_201_CREATED
    return await service.create_sent_email(input_data)


@router.get(
    '/month_counter',
    responses={
        200: {'model': CounterSchema, 'description': 'The counter of sent emails for the current month'},
    },
)
async def sent_emails_month_count(
    from_email: str = DEFAULT_FROM_EMAIL,
    user: ServiceUserSchema = Depends(get_current_user),
    service: SentEmailService = Depends(get_sent_email_service),
):
    """Sent emails count in the current month."""
    recipient_count = await service.get_recipient_month_count(from_email)
    return {'recipient_count': recipient_count}


@router.get(
    '/{sent_email_id}',
    response_model=SentEmailSchema,
    responses={
        200: {'model': SentEmailSchema, 'description': 'Sent email'},
        404: {'model': ErrorMessage, 'description': 'Sent email not found'},
    },
)
async def get_sent_email(
    sent_email_id: int,
    user: ServiceUserSchema = Depends(get_current_user),
    service: SentEmailService = Depends(get_sent_email_service),
):
    """Getting information on a specific sent email."""
    try:
        sent_email_data = await service.get_sent_email(sent_email_id)
    except NotFoundException:
        raise NotFoundError

    return sent_email_data
