from sqlalchemy.orm.session import Session
from models.admin_model import Admin, AdminBase
from models.sales_model import Sales, SalesBase
from fastapi.responses import JSONResponse
from helpers.myfunctions import hash_password
import pyotp


# insert sales
def create_admin(db: Session, reg: AdminBase):
    # insert ke sales dgn hash password
    sales = db.query(Admin).filter(Admin.email == reg.email).first()
    if sales:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Admin allready exists",
            },
        )

    data = Admin(
        fullname=reg.fullname,
        email=reg.email,
        password=hash_password(reg.password),
        phone=reg.phone,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    # di verifiedkan
    return {"message": "Admin baru ditambahkan"}


def get_admin_by_email(db: Session, email: str):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin:
        return admin

    return JSONResponse(
        status_code=400,
        content={
            "message": "Admin not found",
        },
    )


def get_admin_dashboard():
    return {"message": "Dashboard"}


def create_sales(db: Session, req: SalesBase):
    data = Sales(
        fullname=req.fullname,
        code=req.code,
        email=req.email,
        password=req.password,
        phone=req.phone,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    return {"message": "Sales berhasil di tambah"}
