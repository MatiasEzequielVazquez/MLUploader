import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MercadoLibre
    ML_CLIENT_ID = os.getenv('ML_CLIENT_ID')
    ML_CLIENT_SECRET = os.getenv('ML_CLIENT_SECRET')
    ML_REDIRECT_URI = os.getenv('ML_REDIRECT_URI')
    ML_ACCESS_TOKEN = os.getenv('ML_ACCESS_TOKEN')
    ML_REFRESH_TOKEN = os.getenv('ML_REFRESH_TOKEN')
    ML_API_BASE = 'https://api.mercadolibre.com'
    
    # Google
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
    GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE')
    GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    # General
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 10))
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.readonly'
    ]