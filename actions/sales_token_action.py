from sqlalchemy.orm.session import Session
from models.sales_token_model import SalesToken
from sqlalchemy.dialects.postgresql import UUID

def update_token(db: Session, id: UUID, token: UUID):
    ct = db.query(SalesToken).filter(SalesToken.id==id).first()
    if (ct):
        ct.update({SalesToken.token:token})
        db.commit()
    else:
        data = SalesToken(sales_id=id,token=token)
        db.add(data)
        db.commit()
        db.refresh(data)
    return True    