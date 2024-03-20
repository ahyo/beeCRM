from sqlalchemy.orm.session import Session
from models.client_token_model import ClientToken
from sqlalchemy.dialects.postgresql import UUID

def update_token(db: Session, id: UUID, token: UUID):
    ct = db.query(ClientToken).get(id)
    if (ct):
        ct.update({ClientToken.token:token})
        db.commit()
    else:
        data = ClientToken(client_id=id,token=token)
        db.add(data)
        db.commit()
        db.refresh(data)
    return True    