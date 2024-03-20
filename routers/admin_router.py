from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.db import get_db
from sqlalchemy.orm.session import Session
from models.admin_model import Admin,AdminBase
from fastapi.responses import JSONResponse, RedirectResponse
from helpers.myfunctions import verify_password
from actions.auth_action import create_access_token
from fastapi.requests import Request
# from actions.sales_token_action import update_token
from actions.admin_action import create_admin

router = APIRouter(
    prefix="/management",
    tags=["Admin"],
)

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
            content={"error":1,"message": "Invalid credential",},
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
