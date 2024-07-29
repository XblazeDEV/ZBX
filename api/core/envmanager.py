import os
from dotenv import load_dotenv

class EnviromentManager:
    def __init__(self):
        load_dotenv()

    def get_mongodb_con(self) -> str:
        return os.getenv("MONGODB_CON")