from models.register_model import Register, RegisterBase, RegisterVerified
from sqlalchemy.orm.session import Session
from helpers.myfunctions import get_random_string, send_register_email, random_number
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
import time
from actions.client_action import create_client
import datetime


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
def update_verified(db: Session, data: RegisterVerified, type: str):
    reg = db.query(Register).filter(Register.email == data.email)
    if type == "otp":
        reg.update(
            {Register.otp_verified: True, Register.otp_date: datetime.datetime.now()}
        )
    else:
        # email verified
        reg.update({Register.verified: True})
    db.commit()


def verify_register_otp(db: Session, data: RegisterVerified):
    reg = (
        db.query(Register)
        .filter(Register.otp_code == data.code)
        .filter(Register.email == data.email)
        .first()
    )
    if not reg:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Invalid verification otp code",
            },
        )
    if reg.otp_verified:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Otp sudah verified",
            },
        )
    update_verified(db, data, "otp")
    return create_client(db, reg)


def verify_register_email(db: Session, data: RegisterVerified):
    reg = (
        db.query(Register)
        .filter(Register.verification_code == data.code)
        .filter(Register.email == data.email)
        .first()
    )
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
    update_verified(db, data, "email")
    return {"message": "Email berhasil di verified"}
