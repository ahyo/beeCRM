from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.db import get_db
from sqlalchemy.orm.session import Session
from models.sales_model import Sales,SalesBase
from fastapi.responses import JSONResponse, RedirectResponse
from helpers.myfunctions import verify_password
from actions.auth_action import create_access_token
from fastapi.requests import Request
from actions.sales_token_action import update_token
from actions.sales_action import create_sales

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)

@router.post("/", response_model=None)
async def sales_register(request: SalesBase, db: Session = Depends(get_db)):
    return create_sales(db, request)

@router.post("/login")
async def sales_login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    sales = db.query(Sales).filter(Sales.email == request.username).first()
    if not sales:
        return JSONResponse(
            status_code=400,
            content={"error":1,"message": "Invalid credential",},
        )
    if not verify_password(sales.password, request.password):
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid credentials"},
        )

    access_token = create_access_token(data={"email": sales.email})
    
    update_token(db,sales.id,access_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "sales_id": sales.id,
        "sales_email": sales.email,
        "sales_fullname": sales.fullname,
    }


@router.post("/logout")
async def sales_logout(request: Request):
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response
