from fastapi import FastAPI, WebSocket, Request, Depends, Response

from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger
from sqlalchemy.orm import Session

from typing import List

from schemas import TalkRequest, TalkRequestCreate, FriendRequestBase, FriendRequest, FriendRequestCreate, TalkRequestBase
from crud import get_talklist, add_talklist, db_register_user, get_friendlist, add_friendlist, get_highest_talklist_index
from models import Base, Talklist, User
from database import SessionLocal, engine

class NotAuthenticatedException(Exception):
    pass

SECRET = "super-secret-key"
app = FastAPI()
login_manager = LoginManager(SECRET, '/', use_cookie=True,
                             custom_exception=NotAuthenticatedException)

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url='/')

Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory = "templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.append(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

def get_user2(userid: str, password: str, db: Session = None):
    if not db:
        with SessionLocal() as db:
            return db.query(User).filter(User.id == userid, User.password == password).first()
    return db.query(User).filter(User.id == userid, User.password == password).first()

@login_manager.user_loader
def get_user(userid: str, db: Session = None):
    if not db:
        with SessionLocal() as db:
            return db.query(User).filter(User.id == userid).first()
    return db.query(User).filter(User.id == userid).first()

@app.post('/register')
def register_user(response: Response,
                  data: OAuth2PasswordRequestForm = Depends(),
                  db: Session = Depends(get_db)):
    id = data.username
    password = data.password

    user = db_register_user(db, id, password)
    if user:
        access_token = login_manager.create_access_token(
            data = {'sub' : id}
        )
        login_manager.set_cookie(response, access_token)
        return "User created"
    else:
        return "Failed"

@app.post("/token")
def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
    id = data.username
    password = data.password

    user = get_user2(id, password)
    if not user:
        raise InvalidCredentialsException
    access_token = login_manager.create_access_token(data={"sub": id})

    login_manager.set_cookie(response, access_token)
    return {"access_token": access_token}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{data}")
    except Exception as e:
        pass
    finally:
        await manager.disconnect(websocket)

@app.get("/")
async def client(request: Request):
    return templates.TemplateResponse("main.html", {"request":request})

@app.get("/talk")
async def client(request: Request):
    return templates.TemplateResponse("talk.html", {"request":request})

@app.get("/friends")
async def client(request: Request):
    return templates.TemplateResponse("friends.html", {"request":request})

@app.get("/talk_list")
async def client(request: Request):
    return templates.TemplateResponse("talk_list.html", {"request":request})

@app.get("/gettalk_list", response_model=List[TalkRequest])
def get_data(db: Session = Depends(get_db), user = Depends(login_manager)):
    return get_highest_talklist_index(db, user)

@app.get("/getfriend", response_model=List[FriendRequest])
def get_friend(db = Depends(get_db), user = Depends(login_manager)):
    return get_friendlist(db, user)

@app.post("/postfriend", response_model=List[FriendRequest])
def post_friend(friend: FriendRequest, db: Session = Depends(get_db), user = Depends(login_manager)):
    return add_friendlist(db, user, friend)

@app.get("/register_page")
async def client(request: Request):
    return templates.TemplateResponse("register.html", {"request":request})

@app.get("/gettalklist", response_model=List[TalkRequest])
def get_data(db: Session = Depends(get_db), user = Depends(login_manager)):
    return get_talklist(db, user)

@app.post("/posttalk", response_model=List[TalkRequest])
def post_talk(talk_req: TalkRequestCreate, db: Session = Depends(get_db), user = Depends(login_manager)):
    return add_talklist(db, talk_req, user)

def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()