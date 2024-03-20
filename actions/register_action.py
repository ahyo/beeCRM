from models.register_model import Register, RegisterBase
from sqlalchemy.orm.session import Session
from helpers.myfunctions import get_random_string, send_register_email, random_number
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
import time
from actions.client_action import create_client


def create_register(db: Session, request: RegisterBase):
    check = db.query(Register).filter(Register.email == request.email).first()
    if check:
        return JSONResponse(
            status_code=400,
            content={"message": "Email sudah terdaftar"},
        )
    data = Register(
        fullname=request.fullname,
        email=request.email,
        password=request.password,
        phone=request.phone,
        reff_code=request.reff_code,
        reff_source=request.reff_source,
        verified=False,
        verification_code=f"{get_random_string(32)}{time.time_ns()}",
        otp_code=f"{random_number(5)}",
        otp_verified=False,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    bt = BackgroundTasks()
    bt.add_task(send_register_email(data))
    return {
        "message": "Pendaftaran Berhasil, silahkan cek email untuk verifikasi",
    }


# update register verified flag
def update_verified(db: Session, code: str):
    reg = db.query(Register).filter(Register.verification_code == code)
    reg.update({Register.verified: True})
    db.commit()


def verify_register(db: Session, code: str):
    reg = db.query(Register).filter(Register.verification_code == code).first()
    if not reg:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Invalid verification code",
            },
        )
    if reg.verified:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Email sudah verified",
            },
        )
    update_verified(db, code)
    return create_client(db, reg)
