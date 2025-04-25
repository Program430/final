from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.environ.get('POSTGRES_DB')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('POSTGRES_PORT')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
ADMIN_SECRET_KEY = os.environ.get('POSTGRES_PASSWORD')

JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
SECRET_KEY_BETWEEN_SERVISES = os.environ.get('SECRET_KEY_BETWEEN_SERVISES')

ADMIN_SERVISE_ADRESS = os.environ.get('ADMIN_SERVISE_ADRESS')
