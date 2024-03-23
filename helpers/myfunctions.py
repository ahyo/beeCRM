import random
import string
from passlib.context import CryptContext
from .send_email import sendEmail
from pyqrcode import QRCode
import pyotp
import datetime
from random import choice


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_ctx.hash(password)


def verify_password(hash, password):
    return pwd_ctx.verify(password, hash)


def send_register_email(register):
    pass
    # host = "http://localhost:8000"
    # link = host + f"/register/verify/{register.verification_code}"
    # sendEmail(
    #     to="ahyo.haryanto@gmail.com",
    #     subject="Verifikasi Pendaftaran",
    #     message=f"Klik link berikut ini {link}",
    # )


def random_number(p):
    otp = "".join(choice(string.digits) for _ in range(p))
    return otp


def generate_totp():
    code = pyotp.random_base32()
    return code


def generate_totp_uri(str):
    totp = pyotp.totp.TOTP(str)
    totp.at(datetime.datetime.now())
    uri = totp.provisioning_uri(name="ahyo.haryanto@gmail.com", issuer_name="beeCRM")
    return uri


def generate_qrcode(str):
    code = QRCode(str)
    image_as_str = code.png_as_base64_str(scale=5)
    html_img = '<img src="data:image/png;base64,{}">'.format(image_as_str)
    return html_img


def verify_otp(uri, otp):
    totp = pyotp.parse_uri(uri)
    return totp.verify(otp)
