import requests
from config import Config

def get_test_user_token():
    """Obtiene un token usando el método de client credentials"""
    
    print("Obteniendo token de acceso para MercadoLibre\n")
    
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": Config.ML_CLIENT_ID,
        "client_secret": Config.ML_CLIENT_SECRET
    }
    
    print("Intentando obtener token...")
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        access_token = data['access_token']
        
        print("\nToken obtenido exitosamente!\n")
        print("IMPORTANTE: Este token es limitado y solo sirve para lectura.")
        print("Para publicar items, necesitás autorizar con tu usuario.\n")
        print(f"ML_ACCESS_TOKEN={access_token}")
        print("\nPero este método NO va a funcionar para publicar...\n")
        return False
    else:
        print(f"\nError: {response.text}\n")
        return False

def manual_auth_instructions():
    """Muestra instrucciones para autorización manual"""
    
    print("="*70)
    print("MÉTODO MANUAL DE AUTORIZACIÓN")
    print("="*70)
    print("\nComo tu app no está certificada, seguí estos pasos:\n")
    
    auth_url = (
        f"https://auth.mercadolibre.com.ar/authorization?"
        f"response_type=code&"
        f"client_id={Config.ML_CLIENT_ID}&"
        f"redirect_uri=https://ejemplo.com/callback"
    )
    
    print("1. Abrí esta URL en tu navegador (copiala completa):\n")
    print(f"   {auth_url}\n")
    
    print("2. Iniciá sesión con tu cuenta de MercadoLibre")
    print("3. Autorizá la aplicación")
    print("4. Vas a ser redirigido a una página que no existe")
    print("5. En la barra de direcciones vas a ver algo como:")
    print("   https://ejemplo.com/callback?code=TG-xxxxxxxxx")
    print("6. COPIÁ ese código que empieza con 'TG-'\n")
    
    code = input("Pegá el código aquí (solo la parte TG-xxxxx): ").strip()
    
    if not code:
        print("\nNo ingresaste ningún código")
        return
    
    # Intercambiar el código por tokens
    print("\nIntercambiando código por tokens...")
    
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": Config.ML_CLIENT_ID,
        "client_secret": Config.ML_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "https://ejemplo.com/callback"
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("\n" + "="*70)
        print("TOKENS OBTENIDOS EXITOSAMENTE!")
        print("="*70)
        print("\nAgregá estas líneas a tu archivo .env:\n")
        print(f"ML_ACCESS_TOKEN={data['access_token']}")
        print(f"ML_REFRESH_TOKEN={data['refresh_token']}")
        print("\n" + "="*70)
    else:
        print(f"\nError obteniendo tokens: {response.json()}")

def main():
    print("\n" + "="*70)
    print("AUTENTICACIÓN CON MERCADOLIBRE")
    print("="*70 + "\n")
    
    # Primero intentar con client credentials (no sirve para publicar)
    get_test_user_token()
    
    # Mostrar método manual
    print("\nVamos a usar el método manual...\n")
    manual_auth_instructions()

if __name__ == "__main__":
    main()