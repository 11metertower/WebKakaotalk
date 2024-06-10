from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    index: Optional[int]
    id: str
    password: str

    class Config:
        orm_mode = True

class TalkRequestBase(BaseModel):
    id: str
    user: str
    talk: str
    time: str
    oppo: str

class TalkRequestCreate(TalkRequestBase):
    pass

class TalkRequest(TalkRequestBase):
    index: Optional[int]

    class Config:
        orm_mode = True

class FriendRequestBase(BaseModel):
    id: Optional[str]

class FriendRequestCreate(FriendRequestBase):
    pass

class FriendRequest(FriendRequestBase):
    id: Optional[str]

    class Config:
        orm_mode = True