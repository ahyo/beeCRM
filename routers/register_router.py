from fastapi import APIRouter, Depends
from models.register_model import RegisterBase, RegisterDisplay
from actions.register_action import create_register, verify_register
from sqlalchemy.orm.session import Session
from config.db import get_db
from helpers.send_email import sendEmail

router = APIRouter(prefix="/register", tags=["Register"])


@router.post("/", response_model=None)
async def client_register(request: RegisterBase, db: Session = Depends(get_db)):
    return create_register(db, request)


@router.get("/verify/{code}")
async def client_register_verify(code: str, db: Session = Depends(get_db)):
    return verify_register(db, code)


# test kirim email
@router.get("/email")
async def test_email():
    sendEmail()
    return {"message": "email verifikasi pendaftaran dikirim"}
