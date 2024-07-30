import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client


class DatabaseManager:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, filename="logs.log", filemode="w")
        load_dotenv()
        self.url: str = os.environ["DATABASE_URL"]
        self.key: str = os.environ["DATABASE_KEY"]

        logging.debug("url: %s", self.url)
        self.db: Client = create_client(self.url, self.key)

    def get_user(self, usremail: str, usrpass: str) -> str:
        try:
            response = self.db.auth.sign_in_with_password({"email": usremail, "password": usrpass})
        except Exception as e:
            return str(e)
        else:
            return "success 200"