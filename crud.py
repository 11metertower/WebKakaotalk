from sqlalchemy.orm import Session
from sqlalchemy import asc, desc, func
from models import User, Talklist, Friendlist
from schemas import TalkRequest, FriendRequest

def db_register_user(db: Session, id, password):
    db_item = User(id = id, password = password)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_talklist(db: Session, user: User):
    return db.query(Talklist).filter((User.id == Talklist.id) | (User.id == Talklist.user), Talklist.owner_index == user.index).order_by(asc(Talklist.index)).all()

def add_talklist(db: Session, item: TalkRequest, user: User):
    db_item = Talklist(id = item.id, user = item.user, talk = item.talk, time = item.time, oppo = item.oppo, owner_index = user.index, owner = user)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db.query(Talklist).all()

def get_friendlist(db: Session, user: User):
    return db.query(Friendlist).filter(Friendlist.owner_index == user.index).all()

def add_friendlist(db: Session, user: User, item: FriendRequest):
    db_item = Friendlist(id = item.id, owner_index = user.index, owner = user)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db.query(Friendlist).all()

def get_highest_talklist_index(db: Session, user: User):
    subquery_oppo = (
        db.query(
            Talklist.oppo.label('sub_oppo'),
            func.max(Talklist.index).label('max_index')
        )
        .filter(Talklist.owner_index == user.index)
        .group_by(Talklist.oppo)
        .subquery()
    )

    result = (
        db.query(Talklist)
        .join(subquery_oppo, (Talklist.index == subquery_oppo.c.max_index))
        .all()
    )
    return result