from fastapi import APIRouter, Depends
from models.register_model import RegisterBase, RegisterVerified
from actions.register_action import (
    create_register,
    verify_register_email,
    verify_register_otp,
)
from sqlalchemy.orm.session import Session
from config.db import get_db
from helpers.send_email import sendEmail

router = APIRouter(prefix="/register", tags=["Register"])


@router.post("/", response_model=None)
async def client_register(request: RegisterBase, db: Session = Depends(get_db)):
    return create_register(db, request)


@router.post("/verify/otp")
async def post_register_otp(request: RegisterVerified, db: Session = Depends(get_db)):
    return verify_register_otp(db, request)


@router.post("/verify/email")
async def post_register_email(request: RegisterVerified, db: Session = Depends(get_db)):
    return verify_register_email(db, request)


# test kirim email
@router.get("/email")
async def test_email():
    sendEmail()
    return {"message": "email verifikasi pendaftaran dikirim"}
