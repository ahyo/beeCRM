from fastapi import FastAPI, Request, status, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# router
from routers import (
    master_router,
    register_router,
    auth_router,
    client_router,
    sales_router,
    admin_router,
)

# model BASE
from models.client_model import Base as ClientBase
from models.sales_model import Base as SalesBase
from models.wp_model import Base as WpBase
from models.register_model import Base as RegiterBase
from models.client_token_model import Base as ClientTokenBase
from models.sales_token_model import Base as SalesTokenBase
from models.admin_model import Base as AdminBase
from models.bank_model import Base as BankBase
from models.provinces_model import Base as ProvinceBase
from models.regencies_model import Base as RegenciesBase
from models.districts_model import Base as DistrictsBase
from models.villages_model import Base as VillagesBase
from models.jobs_model import Base as JobsBase
from models.countries_model import Base as CountriesBase

from config.db import engine

from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi_pagination import add_pagination

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

description = """
bee CRM API. 🚀
## Client Registration
You can **register** with lead sources tracking.
## CDD
"""

app = FastAPI(
    docs_url="/documentation",
    redoc_url=None,
    title="beeCRM",
    description=description,
    summary="Customer Relationship Management.",
    version="1.0",
    terms_of_service="",
    contact={
        "name": "Ahyo Haryanto",
        "url": "https://syafasoft.com",
        "email": "ahyo.haryanto@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ROUTER
app.include_router(register_router.router)
app.include_router(client_router.router)
app.include_router(auth_router.router)
app.include_router(sales_router.router)
app.include_router(admin_router.router)
app.include_router(master_router.router)

add_pagination(app)


# favico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")


# EXCEPTIONS
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    error = exc.errors()[0]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"message": error["loc"][1] + " " + error["msg"], "body": exc.body}
        ),
    )


# CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATABASE
ClientBase.metadata.create_all(engine)
SalesBase.metadata.create_all(engine)
WpBase.metadata.create_all(engine)
RegiterBase.metadata.create_all(engine)
ClientTokenBase.metadata.create_all(engine)
SalesTokenBase.metadata.create_all(engine)
AdminBase.metadata.create_all(engine)

# MASTER DATA
BankBase.metadata.create_all(engine)
ProvinceBase.metadata.create_all(engine)
RegenciesBase.metadata.create_all(engine)
DistrictsBase.metadata.create_all(engine)
VillagesBase.metadata.create_all(engine)
JobsBase.metadata.create_all(engine)
CountriesBase.metadata.create_all(engine)
