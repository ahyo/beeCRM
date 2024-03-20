from sqlalchemy.orm.session import Session
from models.sales_model import Sales,SalesBase
from fastapi.responses import JSONResponse
from helpers.myfunctions import hash_password


# insert sales
def create_backoffice(db: Session, reg: SalesBase):
    # insert ke sales dgn hash password
    sales = db.query(Sales).filter(Sales.email == reg.email).first()
    if sales:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Sales allready exists",
            },
        )

    data = Sales(
        fullname=reg.fullname,
        email=reg.email,
        password=hash_password(reg.password),
        phone=reg.phone,
        code=reg.code
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    # di verifiedkan
    return {"message": "Sales baru ditambahkan"}


def get_backoffice_by_email(db: Session, email: str):
    client = db.query(Sales).filter(Sales.email == email).first()
    if client:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Sales not found",
            },
        )
    return client


def get_backoffice_dashboard():
    return {"message": "Dashboard"}
