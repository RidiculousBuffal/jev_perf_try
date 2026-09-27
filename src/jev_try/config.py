import os

import dotenv

dotenv.load_dotenv()


class Config:
    JEV_BASE_URL = os.getenv("JEV_BASE_URL")
    JEV_API_KEY = os.getenv("JEV_API_KEY")
