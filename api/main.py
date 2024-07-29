import base64
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .core import LogForm, EnviromentManager, DatabaseManager

api = FastAPI()

ENVIRONS = EnviromentManager()

auth_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_pass(usrpass: str, encpass: str) -> bool:
    decpass = base64.b64decode(encpass.encode()).decode()
    return usrpass == decpass

@api.get("/")
def hello():
    return {"200": "success"}

@api.post("/login")
async def get_user(usrform: OAuth2PasswordRequestForm = Depends()):
    db = DatabaseManager(usrform.username, ENVIRONS.get_mongodb_con())
    usrdata: list[str] = db.get_data()

    if usrdata == ["404"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found",
            headers={"WWW-Authenticate": "Bearer"}
        )