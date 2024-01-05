from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import UJSONResponse
from finbot_platform.settings import settings
from finbot_platform.web.api.router import api_router

def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    app = FastAPI(
        title="Finbot Platform API",
        version="1.0.0",
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], #TODO: ONLY FRONTEND URL SHOULD BE HERE
        allow_origin_regex=settings.allowed_origins_regex,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # # Adds startup and shutdown events.
    # register_startup_event(app)
    # register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    #
    # app.exception_handler(PlatformaticError)(platformatic_exception_handler)

    return app