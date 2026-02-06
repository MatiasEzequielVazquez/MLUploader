import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io
from typing import List
from config import Config
from models import Product

class GoogleClient:
    def __init__(self):
        self.creds = Credentials.from_service_account_file(
            Config.GOOGLE_CREDENTIALS_FILE,
            scopes=Config.SCOPES
        )
        self.sheets_client = gspread.authorize(self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        
    def get_pending_products(self) -> List[Product]:
        """Lee productos pendientes del sheet"""
        sheet = self.sheets_client.open_by_key(Config.GOOGLE_SHEET_ID).sheet1
        rows = sheet.get_all_values()[1:]  # Skip header
        
        products = []
        for idx, row in enumerate(rows, start=2):  # Start at 2 (header is 1)
            # Solo procesar filas con status vacío o 'pending'
            status = row[10] if len(row) > 10 else ""
            if status in ["", "pending"]:
                product = Product.from_sheet_row(row, idx)
                products.append(product)
                
        return products[:Config.BATCH_SIZE]
    
    def update_product_status(self, product: Product):
        """Actualiza el status de un producto en el sheet"""
        sheet = self.sheets_client.open_by_key(Config.GOOGLE_SHEET_ID).sheet1
        
        # Columnas: J=ML_ID (10), K=Status (11), L=Error (12)
        updates = [
            (product.row_number, 10, product.ml_id or ""),
            (product.row_number, 11, product.status),
            (product.row_number, 12, product.error_message or "")
        ]
        
        for row, col, value in updates:
            sheet.update_cell(row, col, value)
    
    def download_image(self, file_id: str, destination: str) -> bool:
        """Descarga una imagen de Drive"""
        try:
            request = self.drive_service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
            
            with open(destination, 'wb') as f:
                f.write(fh.getvalue())
            
            return True
        except Exception as e:
            print(f"Error descargando imagen {file_id}: {str(e)}")
            return False