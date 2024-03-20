from fastapi import APIRouter, Depends, UploadFile
from actions.client_action import get_dashboard, upload_dokumen
from sqlalchemy.orm.session import Session
from models.client_model import Client, ClientAuth, dokumenEnum
from actions.auth_action import get_current_client
from config.db import get_db
import os
from typing import Annotated

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
    current_client: Annotated[Client, Depends(get_current_client)],
    db: Session = Depends(get_db),
    # current_client: ClientAuth = Depends(get_current_client),
):
    return upload_dokumen(file, types, current_client)
