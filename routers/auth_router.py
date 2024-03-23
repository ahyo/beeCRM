from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config.db import get_db
from sqlalchemy.orm.session import Session
from models.client_model import Client
from fastapi.responses import JSONResponse, RedirectResponse
from helpers.myfunctions import verify_password
from actions.auth_action import create_access_token
from fastapi.requests import Request

router = APIRouter(
    tags=["Auth"],
)


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    client = db.query(Client).filter(Client.email == request.username).first()
    if not client:
        return JSONResponse(
            status_code=400,
            content={
                "error": 1,
                "message": "Invalid credential",
            },
        )
    if not verify_password(client.password, request.password):
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid credentials"},
        )

    access_token = create_access_token(data={"email": client.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "client_id": client.id,
        "client_email": client.email,
        "client_fullname": client.fullname,
    }


@router.post("/logout")
async def logout(request: Request):
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response
