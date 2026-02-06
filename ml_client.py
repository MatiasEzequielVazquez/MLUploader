import requests
from typing import List, Optional, Tuple
from config import Config

class MLClient:
    def __init__(self):
        self.base_url = Config.ML_API_BASE
        self.access_token = Config.ML_ACCESS_TOKEN
        
    def _headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def refresh_access_token(self) -> bool:
        """Refresca el access token usando el refresh token"""
        url = f"{self.base_url}/oauth/token"
        payload = {
            'grant_type': 'refresh_token',
            'client_id': Config.ML_CLIENT_ID,
            'client_secret': Config.ML_CLIENT_SECRET,
            'refresh_token': Config.ML_REFRESH_TOKEN
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            # Aquí se debería actualizar el .env o usar otro método de persistencia
            print("✓ Token refrescado exitosamente")
            return True
        
        print(f"✗ Error refrescando token: {response.text}")
        return False
    
    def upload_image(self, image_path: str) -> Optional[str]:
        """Sube una imagen a ML y retorna la URL"""
        url = f"{self.base_url}/pictures"
        
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            response = requests.post(url, headers=self._headers(), files=files)
        
        if response.status_code == 200:
            return response.json()['secure_url']
        
        print(f"✗ Error subiendo imagen: {response.text}")
        return None
    
    def create_listing(self, payload: dict) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Crea una publicación en ML
        Returns: (success, ml_id, error_message)
        """
        url = f"{self.base_url}/items"
        response = requests.post(url, headers=self._headers(), json=payload)
        
        if response.status_code == 201:
            ml_id = response.json()['id']
            return True, ml_id, None
        
        error_msg = response.json().get('message', response.text)
        return False, None, error_msg
    
    def validate_category(self, category_id: str) -> bool:
        """Valida que la categoría exista"""
        url = f"{self.base_url}/categories/{category_id}"
        response = requests.get(url)
        return response.status_code == 200