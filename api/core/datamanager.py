import pymongo
from pymongo import MongoClient
import pymongo.errors
import logging


class DatabaseManager:
    def __init__(self, name: str, constr: str) -> None:
        logging.basicConfig(level=logging.DEBUG, filename="test.log", filemode="w")

        self.name: str = name
        self.constr: str = constr

        try:
            self.client = MongoClient(constr)
        except pymongo.errors.ServerSelectionTimeoutError:
            raise self.ZBX_TIMEOUT("Database timeout")
        
        logging.debug("passed line 13 btw")

        self.db = self.client.zbx
        self.col = self.db.users

    def get_data(self) -> list[str]:
        try:
            response = self.col.find_one({"usrname": self.name})
        except pymongo.errors.ServerSelectionTimeoutError:
            return["500"]

        if response is None:
            return ["404"]
        else:
            data: list[str] = []
            for info in response:
                data.append(info)

            return data
        
    def add_data(self, to_add: dict) -> dict:
        response = self.col.insert_one(to_add)

        return {"ID": str(response.inserted_id)}
    
    class ZBX_TIMEOUT(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)