from pydantic import BaseModel

class LogForm(BaseModel):
    usrname: str
    usrpass: str