from sqlalchemy.orm.session import Session
from models.admin_model import Admin, AdminBase
from fastapi.responses import JSONResponse
from helpers.myfunctions import hash_password


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
        phone=reg.phone
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    # di verifiedkan
    return {"message": "Admin baru ditambahkan"}


def get_admin_by_email(db: Session, email: str):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if admin:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Sales not found",
            },
        )
    return admin


def get_admin_dashboard():
    return {"message": "Dashboard"}
