from fastapi import APIRouter, Depends, UploadFile
from actions.client_action import (
    get_dashboard,
    upload_dokumen,
    client_identity,
    client_address,
    client_personal,
    client_job,
    client_bank,
)
from actions.auth_action import get_current_client

from config.db import get_db
import os
from typing import List, Literal
from sqlalchemy.orm.session import Session


from models.client_model import ClientAuth, ClientUpdate
from models.client_address_model import ClientAddressUpdate
from models.client_personal_model import ClientPersonalUpdate
from models.client_job_model import ClientJobUpdate
from models.client_bank_model import ClientBankUpdate


router = APIRouter(tags=["Client"])


@router.get("/")
async def client_index(
    db: Session = Depends(get_db),
    current_client: ClientAuth = Depends(get_current_client),
):
    return get_dashboard()


@router.post("/dokumen")
async def post_upload_dokumen(
    file: UploadFile,
    types: str,
    db: Session = Depends(get_db),
    current_client: ClientAuth = Depends(get_current_client),
):
    return upload_dokumen(file, types, current_client)


@router.post("/identity")
async def update_client_identity(
    request: ClientUpdate,
    db: Session = Depends(get_db),
    current_client: ClientAuth = Depends(get_current_client),
):
    return client_identity(db, request, current_client.id)


@router.post("/address")
async def update_client_address(
    request: ClientAddressUpdate,
    db: Session = Depends(get_db),
    current_client: ClientAuth = Depends(get_current_client),
):
    return client_address(db, request, current_client.id)


@router.post("/personal")
async def update_client_personal(
    request: ClientPersonalUpdate,
    db: Session = Depends(get_db),
    current_client: ClientAuth = Depends(get_current_client),
):
    return client_personal(db, request, current_client.id)


@router.post("/job")
async def update_client_job(
    request: ClientJobUpdate,
    db: Session = Depends(get_db),
    current_client: ClientAuth = Depends(get_current_client),
):
    return client_job(db, request, current_client.id)


@router.post("/bank")
async def update_client_bank(
    request: ClientBankUpdate,
    db: Session = Depends(get_db),
    current_client: ClientAuth = Depends(get_current_client),
):
    return client_bank(db, request, current_client.id)
