import base64
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .core import LogForm, EnviromentManager, DatabaseManager

api = FastAPI()

ENVIRONS = EnviromentManager()

auth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_pass(usrpass: str, encpass: str) -> bool:
    decpass = base64.b64decode(encpass.encode()).decode()
    return usrpass == decpass

@api.get("/")
def hello():
    return {"200": "success"}

@api.post("/login")
async def login(usrform: OAuth2PasswordRequestForm = Depends()):
    db = DatabaseManager(usrform.username, ENVIRONS.get_mongodb_con())
    usrdata: list[str] = db.get_data()

    if usrdata == ["404"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="404. No user found"
        )
    elif usrdata == ["500"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="500. Error while connecting to the database"
        )
    
    if not verify_pass(usrform.password, usrdata[2]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401. Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return {"200": "success", "data": usrdata}

@api.get("/user")
async def get_user(token: str = Depends(auth_scheme)):
    try:
        db = DatabaseManager(token, ENVIRONS.get_mongodb_con())
    except DatabaseManager.ZBX_TIMEOUT:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="500. Error while connecting to database"
        )
    usrdata: list[str] = db.get_data()

    if usrdata == ["404"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="404. No user found"
        )
    
    return {"usrname": usrdata[1], "usremail": usrdata[3]}

@api.post("/sign")
async def mk_user(user: LogForm):
    db = DatabaseManager(user.usrname, ENVIRONS.get_mongodb_con())
    usrdata: list[str] = db.get_data()

    if not usrdata == ["404"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="400. User already exists"
        )
    
    usradd: LogForm = LogForm(user.usrname, base64.b64decode(user.usrpass.encode()).decode(), user.usremail)

    res = db.add_data(usradd.model_dump())

    return {"200": "success", "id": res["ID"]}