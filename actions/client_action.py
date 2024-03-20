from sqlalchemy.orm.session import Session
from models.client_model import Client
from models.register_model import RegisterBase
from fastapi.responses import JSONResponse
from helpers.myfunctions import hash_password
import os
from models.client_model import Client, ClientAuth
import json
from pydantic import parse_obj_as
import filetype


# insert client
def create_client(db: Session, reg: RegisterBase):
    # insert ke client dgn hash password
    client = db.query(Client).filter(Client.email == reg.email).first()
    if client:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Client allready exists",
            },
        )

    data = Client(
        fullname=reg.fullname,
        email=reg.email,
        password=hash_password(reg.password),
        phone=reg.phone,
        register_id=reg.id,
        wp_id=reg.wp_id,
        sales_id=reg.sales_id,
    )
    db.add(data)
    db.commit()
    db.refresh(data)
    # di verifiedkan
    return {"message": "Verified berhasil, silahkan login"}


def get_client_by_email(db: Session, email: str):
    client = db.query(Client).filter(Client.email == email).first()
    if client:
        return JSONResponse(
            status_code=400,
            content={
                "message": "Client not found",
            },
        )
    return client


def get_dashboard():
    return {"message": "Dashboard"}


def upload_dokumen(file, types, current_client):
    # print(current_client)
    try:
        FILE_SIZE = 2097152  # 2MB

        accepted_file_types = [
            "image/png",
            "image/jpeg",
            "image/jpg",
            "image/heic",
            "image/heif",
            "image/heics",
            "png",
            "jpeg",
            "jpg",
            "heic",
            "heif",
            "heics",
        ]
        file_info = filetype.guess(file.file)
        if file_info is None:
            return JSONResponse(
                status_code=415,
                content={"message": "Unable to determine file type"},
            )

        detected_content_type = file_info.extension.lower()

        if (
            file.content_type not in accepted_file_types
            or detected_content_type not in accepted_file_types
        ):
            return JSONResponse(
                status_code=415,
                content={"message": "Unsupported file type"},
            )
        filenya = file.file.read()
        real_file_size = 0
        for chunk in file.file:
            real_file_size += len(chunk)
            if real_file_size > FILE_SIZE:
                return JSONResponse(
                    status_code=413,
                    content={"message": "Too large"},
                )
        # Create a directory named with today's date
        directory = f"./images/"

        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{types}.jpg"
        file_location = f"{directory}/{filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(filenya)

        return {"info": f"file '{filename}' saved at {directory}"}

    except Exception as e:
        return {"error": str(e)}
