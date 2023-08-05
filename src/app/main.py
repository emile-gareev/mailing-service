from fastapi import APIRouter, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from logging import getLogger

from app.config import SETTINGS, HealthCheckSettings
from app.db.models.base import ExternalHealthCheckResponse, HealthCheckValidResponse
from app.db.postgres_health_check import get_postgres_issues
from app.middlewares.exception_handler import exception_handle
from app.routers.internal.v1.sent_email import router as sent_email_router


logger = getLogger('elk')


def init_routes(app_: FastAPI) -> None:
    app_.include_router(sent_email_router, prefix='/api/v1/sent_email', tags=['SentEmails'])


def get_router(settings: HealthCheckSettings) -> APIRouter:
    healthcheck_router = APIRouter()

    if settings.INTERNAL.ENABLED:

        @healthcheck_router.get(
            settings.INTERNAL.PATH,
            response_model=HealthCheckValidResponse,
            responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Error text"}},
        )
        async def internal_health_check():
            if settings.POSTGRES.ENABLED and (err := await get_postgres_issues()):
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=err,
                )
            return HealthCheckValidResponse()

    if settings.EXTERNAL.ENABLED:

        @healthcheck_router.get(
            settings.EXTERNAL.PATH,
            response_model=ExternalHealthCheckResponse,
        )
        async def external_health_check():
            return ExternalHealthCheckResponse()

    return healthcheck_router


def init_health_checks(app: FastAPI, settings: HealthCheckSettings = None) -> FastAPI:
    if not settings:
        settings = HealthCheckSettings()
    if not settings.ENABLED:
        return app
    app.include_router(get_router(settings))
    return app


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=SETTINGS.service_name,
        default_response_class=ORJSONResponse,
        docs_url=f'{SETTINGS.API.ROOT}/docs' if SETTINGS.API.DOCS_ENABLED else None,
        openapi_url=f'{SETTINGS.API.ROOT}/docs/openapi.json' if SETTINGS.API.DOCS_ENABLED else None,
        redoc_url=f'{SETTINGS.API.ROOT}/redocs' if SETTINGS.API.DOCS_ENABLED else None,
        version=SETTINGS.API.VERSION,
    )

    init_routes(app_)
    app_ = init_health_checks(app_)
    return app_


app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def startup() -> None:
    app.middleware('http')(exception_handle)


@app.on_event('shutdown')
async def shutdown() -> None:
    logger.warning('Shutdown')
