import random
import string
from passlib.context import CryptContext
from .send_email import sendEmail


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
    randomlist = random.sample(range(0, 9), p)
    rndstr = (str(i) for i in randomlist)
    return "".join(rndstr)
