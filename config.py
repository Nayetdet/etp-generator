from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Config:
    DATABASE_URI = getenv('DATABASE_URI')
    OPENAI_KEY = getenv('OPENAI_KEY')
