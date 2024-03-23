from fastapi import APIRouter, Depends, Request
from config.db import get_db
from sqlalchemy.orm.session import Session
from models.bank_model import Bank, BankOut
from models.provinces_model import Provices, ProvicesOut
from models.regencies_model import Regencies, RegenciesOut
from models.districts_model import Districts, DistrictsOut
from models.villages_model import Villages, VillagesOut
from models.countries_model import Countries, CountriesOut

from fastapi_pagination import Page
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)


router = APIRouter(
    prefix="/management",
    tags=["Master"],
)


@router.get("/bank")
@limiter.limit("100/minute")
def get_bank_list(request: Request, db: Session = Depends(get_db)) -> Page[BankOut]:
    return paginate(db, select(Bank))


@router.get("/countries")
@limiter.limit("1000/minute")
def get_country_list(
    request: Request, db: Session = Depends(get_db)
) -> Page[CountriesOut]:
    return paginate(db, select(Countries))


@router.get("/provinces")
@limiter.limit("100/minute")
def get_province_list(
    request: Request, db: Session = Depends(get_db)
) -> Page[ProvicesOut]:
    return paginate(db, select(Provices))


@router.get("/regencies")
@limiter.limit("100/minute")
def get_regency_list(
    request: Request, db: Session = Depends(get_db)
) -> Page[RegenciesOut]:
    return paginate(db, select(Regencies))


@router.get("/regencies/{province_id}")
@limiter.limit("100/minute")
def get_regency_province_list(
    province_id: int,
    request: Request,
    db: Session = Depends(get_db),
) -> Page[RegenciesOut]:
    return paginate(db, select(Regencies).filter(Regencies.province_id == province_id))


@router.get("/districts")
@limiter.limit("100/minute")
def get_distric_list(
    request: Request, db: Session = Depends(get_db)
) -> Page[DistrictsOut]:
    return paginate(db, select(Districts))


@router.get("/districts/{regency_id}")
@limiter.limit("100/minute")
def get_distric_list(
    regency_id: int, request: Request, db: Session = Depends(get_db)
) -> Page[DistrictsOut]:
    return paginate(db, select(Districts).filter(Districts.regency_id == regency_id))


@router.get("/villages")
@limiter.limit("100/minute")
def get_village_list(
    request: Request, db: Session = Depends(get_db)
) -> Page[VillagesOut]:
    return paginate(db, select(Villages))


@router.get("/villages/{district_id}")
@limiter.limit("100/minute")
def get_village_list(
    district_id: int, request: Request, db: Session = Depends(get_db)
) -> Page[VillagesOut]:
    return paginate(db, select(Villages).filter(Villages.district_id == district_id))
