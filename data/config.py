import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

admin_id = 478278207
admins = [478278207]

DATA_NAME = os.getenv('DATA_NAME')
PASSWORD_DB = os.getenv('PGPASSWORD')
HOST_DB = os.getenv('PGHOST')
DATABASE = os.getenv('DATABASE')

postgres_uri = f"postgresql://{DATA_NAME}:{PASSWORD_DB}@{HOST_DB}/{DATABASE}"

provider_token = '********'

qiwi_token = os.getenv('QIWI_TOKEN')
qiwi_phone = os.getenv('QIWI_PHONE')
qiwi_key = os.getenv('QIWI_PUBKEY')
