from sqlalchemy.orm.session import Session

from models.register_model import RegisterBase
from fastapi.responses import JSONResponse
from helpers.myfunctions import hash_password
import os
import filetype

from sqlalchemy.dialects.postgresql import UUID
from models.client_model import Client, ClientUpdate
from models.client_address_model import ClientAddress, ClientAddressUpdate
from models.client_bank_model import ClientBank, ClientBankUpdate
from models.client_emergency_model import ClientEmergency
from models.client_job_model import ClientJob, ClientJobUpdate
from models.client_personal_model import ClientPersonal, ClientPersonalUpdate
from models.client_property_model import ClientProperty, ClientPropertyUpdate


def create_client_address(db: Session, id: UUID):
    data = ClientAddress(id=id)
    db.add(data)
    db.commit()
    db.refresh(data)


def create_client_bank(db: Session, id: UUID):
    data = ClientBank(id=id)
    db.add(data)
    db.commit()
    db.refresh(data)


def create_client_emergency(db: Session, id: UUID):
    data = ClientEmergency(id=id)
    db.add(data)
    db.commit()
    db.refresh(data)


def create_client_job(db: Session, id: UUID):
    data = ClientJob(id=id)
    db.add(data)
    db.commit()
    db.refresh(data)


def create_client_personal(db: Session, id: UUID):
    data = ClientPersonal(id=id)
    db.add(data)
    db.commit()
    db.refresh(data)


def create_client_property(db: Session, id: UUID):
    data = ClientProperty(id=id)
    db.add(data)
    db.commit()
    db.refresh(data)


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
        sales_id=reg.sales_id,
    )
    db.add(data)
    db.commit()
    db.refresh(data)

    # relasi table
    create_client_address(db, data.id)
    create_client_bank(db, data.id)
    create_client_emergency(db, data.id)
    create_client_job(db, data.id)
    create_client_personal(db, data.id)
    create_client_property(db, data.id)

    return {"message": "Verified berhasil, silahkan login"}


def get_client_by_email(db: Session, email: str):
    client = db.query(Client).filter(Client.email == email).first()
    if client:
        return client

    return JSONResponse(
        status_code=400,
        content={
            "message": "Client not found",
        },
    )


def get_dashboard():
    return {"message": "Dashboard"}


def upload_dokumen(file, types, current_client):
    # print(current_client)
    valid = ["ktp", "selfie", "npwp_kk"]
    if types not in valid:
        return JSONResponse(status_code=404, content={"message": "Invalid types"})
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
        directory = f"./images/{current_client.id}"

        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{types}.jpg"
        file_location = f"{directory}/{filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(filenya)

        return {"info": f"file '{filename}' saved at {directory}"}

    except Exception as e:
        return {"error": str(e)}


def client_identity(db: Session, request: ClientUpdate, id: UUID):
    client = db.query(Client).filter(Client.id == id)
    if client:
        client.update(
            {
                Client.fullname: request.fullname,
                Client.no_ktp: request.no_ktp,
                Client.birth_date: request.birth_date,
                Client.birth_place: request.birth_place,
                Client.gender: request.gender,
                Client.job: request.job,
                Client.no_npwp: request.no_npwp,
            }
        )
        db.commit()
        return {"message": "Updated"}
    else:
        JSONResponse(
            content={"message": "Not found"},
            status_code=404,
        )


def client_address(db: Session, request: ClientAddressUpdate, id: UUID):
    client = db.query(ClientAddress).filter(ClientAddress.id == id)
    if client:
        client.update(
            {
                ClientAddress.ktp_address: request.ktp_address,
                ClientAddress.ktp_country_id: request.ktp_country_id,
                ClientAddress.ktp_province_id: request.ktp_province_id,
                ClientAddress.ktp_district_id: request.ktp_district_id,
                ClientAddress.ktp_regency_id: request.ktp_regency_id,
                ClientAddress.ktp_village_id: request.ktp_village_id,
                ClientAddress.ktp_post_code: request.ktp_post_code,
                ClientAddress.address: request.address,
                ClientAddress.country_id: request.country_id,
                ClientAddress.province_id: request.province_id,
                ClientAddress.regency_id: request.regency_id,
                ClientAddress.district_id: request.district_id,
                ClientAddress.village_id: request.village_id,
                ClientAddress.post_code: request.post_code,
            }
        )
        db.commit()
        return {"message": "Updated"}
    else:
        JSONResponse(
            content={"message": "Not found"},
            status_code=404,
        )


def client_personal(db: Session, request: ClientPersonalUpdate, id: UUID):
    client = db.query(ClientPersonal).filter(ClientPersonal.id == id)
    if client:
        client.update(
            {
                ClientPersonal.home_phone: request.home_phone,
                ClientPersonal.home_status: request.home_status,
                ClientPersonal.mother_name: request.mother_name,
                ClientPersonal.marital_status: request.marital_status,
                ClientPersonal.spouse_name: request.spouse_name,
            }
        )
        db.commit()
        return {"message": "Updated"}
    else:
        JSONResponse(
            content={"message": "Not found"},
            status_code=404,
        )


def client_job(db: Session, request: ClientJobUpdate, id: UUID):
    client = db.query(ClientJob).filter(ClientJob.id == id)
    if client:
        client.update(
            {
                ClientJob.address: request.address,
                ClientJob.company_name: request.company_name,
                ClientJob.annual_revenue: request.annual_revenue,
                ClientJob.field: request.field,
                ClientJob.position: request.position,
                ClientJob.post_code: request.post_code,
                ClientJob.working_year: request.working_year,
                ClientJob.prev_working_year: request.prev_working_year,
            }
        )
        db.commit()
        return {"message": "Updated"}
    else:
        JSONResponse(
            content={"message": "Not found"},
            status_code=404,
        )


def client_bank(db: Session, request: ClientBankUpdate, id: UUID):
    client = db.query(ClientBank).filter(ClientBank.id == id)
    if client:
        client.update(
            {
                ClientBank.account: request.account,
                ClientBank.account_name: request.account_name,
                ClientBank.name: request.name,
                ClientBank.branch: request.branch,
                ClientBank.rate: request.rate,
                ClientBank.phone: request.phone,
                ClientBank.type: request.type,
            }
        )
        db.commit()
        return {"message": "Updated"}
    else:
        JSONResponse(
            content={"message": "Not found"},
            status_code=404,
        )
