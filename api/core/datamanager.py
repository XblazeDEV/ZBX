from pymongo import MongoClient


class DatabaseManager:
    def __init__(self, name: str, constr: str) -> None:
        self.name: str = name
        self.constr: str = constr

        self.client = MongoClient(constr)
        self.db = self.client.zbx
        self.col = self.db.users

    def get_data(self) -> list[str]:
        response = self.col.find_one({"usrname": self.name})

        if response is None:
            return ["404"]
        else:
            data: list[str] = []
            for info in response:
                data.append(info)

            return data