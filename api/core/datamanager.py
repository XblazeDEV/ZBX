import os
import logging
from dotenv import load_dotenv
from supabase import create_client


class DatabaseManager:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, filename="logs.log", filemode="w")
        load_dotenv()
        self.url: str = os.getenv("DATABASE_URL")
        self.key: str = os.getenv("DATABASE_KEY")

        logging.debug("url: %s", self.url)
        self.database = create_client(self.url, self.key)

    def get_data(self, data: list):
        response = self.database.table("users").select("*").eq("usrname", data[0])
        response.execute()
        
        return response.data if response.data else "404"