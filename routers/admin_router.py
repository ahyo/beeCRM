from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.db import get_db
from sqlalchemy.orm.session import Session
from models.admin_model import Admin, AdminBase, AdminAuth
from models.sales_model import Sales, SalesBase
from fastapi.responses import JSONResponse, RedirectResponse
from helpers.myfunctions import verify_password
from actions.auth_action import create_access_token, get_current_admin
from fastapi.requests import Request

# from actions.sales_token_action import update_token
from actions.admin_action import create_admin, create_sales
from helpers.myfunctions import (
    generate_qrcode,
    generate_totp_uri,
    generate_totp,
    verify_otp,
)

router = APIRouter(
    prefix="/management",
    tags=["Admin"],
)


# sementara untuk add admin
@router.post("/", response_model=None)
async def admin_register(request: AdminBase, db: Session = Depends(get_db)):
    return create_admin(db, request)


@router.post("/login")
async def admin_login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    admin = db.query(Admin).filter(Admin.email == request.username).first()
    if not admin:
        return JSONResponse(
            status_code=400,
            content={
                "error": 1,
                "message": "Invalid credential",
            },
        )
    if not verify_password(admin.password, request.password):
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid credentials"},
        )

    access_token = create_access_token(data={"email": admin.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin_email": admin.email,
        "admin_fullname": admin.fullname,
    }


@router.post("/logout")
async def admin_logout(request: Request):
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie(key="bee_admin_token")
    return response


@router.post("/sales", response_model=None)
async def add_new_sales(
    request: SalesBase,
    db: Session = Depends(get_db),
    current_admin: AdminAuth = Depends(get_current_admin),
):
    return create_sales(db, request)


@router.get("/code")
async def get_code():
    str = generate_totp()
    uri = generate_totp_uri(str)
    code = generate_qrcode(uri)
    return {"str": str, "uri": uri, "qrcode": code}


@router.post("/verify")
async def verify_code(uri: str, otp: str):
    check = verify_otp(uri, otp)
    return {"message": f"verify : {check}"}
