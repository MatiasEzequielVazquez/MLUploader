# MLUploader

Simple herramienta automatizada para carga masiva de productos en MercadoLibre usando Google Sheets como fuente de datos y Google Drive para el almacenamiento de imágenes.

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual
3. Instalar dependencias
4. Configurar variables de entorno


## Configuración

### Google Cloud Platform

#### 1 Crear Proyecto

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Click en "Nuevo Proyecto"
3. Nombre: `MLUploader` (o el que prefieras)
4. Click en "Crear"

#### 2 Habilitar APIs

1. En el menú lateral: **APIs y servicios** → **Biblioteca**
2. Buscar y habilitar:
   - **Google Sheets API**
   - **Google Drive API**

#### 3 Crear Service Account

1. Ir a **APIs y servicios** → **Credenciales**
2. Click en **Crear credenciales** → **Cuenta de servicio**
3. Completar:
   - Nombre: `mluploader-service`
   - Descripción: `Service account para MLUploader`
4. Click en **Crear y continuar**
5. Rol (opcional): **Editor**
6. Click en **Continuar** → **Listo**

#### 4 Descargar Credenciales

1. En la lista de cuentas de servicio, click en la recién creada
2. Pestaña **Claves** → **Agregar clave** → **Crear clave nueva**
3. Tipo: **JSON**
4. Click en **Crear**
5. Renombrar el archivo descargado a `credentials.json`
6. Mover a la raíz del proyecto

#### 5 Copiar Email del Service Account

1. Abrir `credentials.json`
2. Copiar el valor de `"client_email"`
3. Ejemplo: `mluploader-service@project-id.iam.gserviceaccount.com`

### Google Sheets

#### 1 Crear Spreadsheet

1. Ir a [Google Sheets](https://sheets.google.com)
2. Crear nueva hoja: `MLUploader - Productos`
3. Copiar el **Sheet ID** de la URL:
```
   https://docs.google.com/spreadsheets/d/SHEET_ID/edit
```
4. Pegar en `.env` como `GOOGLE_SHEET_ID`

#### 2 Configurar Headers

En la **primera fila**, agregar headers:

| A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Title | Category | Price | Stock | Condition | Listing Type | Description | Images IDs | Free Shipping | ML ID | Status | Error |

#### 3 Compartir Sheet

1. Click en **Compartir**
2. Pegar el **email del service account**
3. Permisos: **Editor**

#### 4 Ejemplo

|  Title  |  Category | Price | Stock | Condition | Listing Type |  Description |      Images IDs     | Free Shipping | ML ID |  Status | Error |
|---------|-----------|-------|-------|-----------|--------------|--------------|---------------------|---------------|-------|---------|-------|
| Botas X | MLA109027 | 89999 |   5   |    new    | gold_special | Botas negras | file_id_1,file_id_2 |      FALSE    |       | pending |       |

**Valores válidos:**
- **Condition**: `new`, `used`, `not_specified`
- **Listing Type**: `gold_special`, `gold_pro`, `free`, `bronze`
- **Free Shipping**: `TRUE` o `FALSE`
- **Status**: `pending` (para procesar), otros valores son automáticos

### Google Drive (Imágenes)

#### 1 Subir Imágenes

1. Crear carpeta en Drive: `MLUploader - Images`
2. Subir imágenes de productos
3. Para cada imagen:
   - Click derecho → **Compartir**
   - Agregar el **email del service account**
   - Permisos: **Lector**

#### 2 Obtener IDs de Archivos

De la URL de cada imagen:
```
https://drive.google.com/file/d/FILE_ID/view
```

En el Sheet, columna **Images IDs**, poner los IDs separados por comas:
```
file_id_1,file_id_2,file_id_3
```

### MercadoLibre Developers

#### 1 Crear Aplicación

1. Ir a [MercadoLibre Developers](https://developers.mercadolibre.com.ar/)
2. **Mis aplicaciones** → **Crear aplicación**
3. Completar:
   - Nombre: `MLUploader`
   - Redirect URI: `https://ejemplo.com/callback` y `https://127.0.0.1:8080`
   - Scopes: Seleccionar permisos de **Items** y **Items Prices**

#### 2 Obtener Credenciales

1. Copiar **Client ID** y **Client Secret**
2. Pegar en `.env`:
```env
   ML_CLIENT_ID=tu_client_id
   ML_CLIENT_SECRET=tu_client_secret
```

#### 3 Certificar Aplicación

Formulario de certificación en MercadoLibre

#### 4 Obtener Tokens de Acceso
```bash
python auth_ml.py
```

Seguir las instrucciones en pantalla:
1. Copiar la URL generada
2. Abrir en navegador
3. Autorizar la aplicación
4. Copiar el código de la URL de redirección
5. Pegar en el script
6. Copiar los tokens generados al `.env`

## Uso

Publicar productos:
```bash
python main.py
```

### Testear Conexión con Google
```bash
python test_google.py
```

## Estructura del Proyecto
```
MLUploader/
├── .env                  # Plantilla de configuración
├── .gitignore            # Archivos ignorados por Git
├── credentials.json      # Credenciales de Google
├── requirements.txt      # Dependencias Python
├── README.md             # Documentación
│
├── config.py             # Configuración de la aplicación
├── models.py             # Modelos de datos
├── validators.py         # Validaciones de productos
├── google_client.py      # Cliente de Google Sheets/Drive
├── ml_client.py          # Cliente de MercadoLibre API
├── uploader.py           # Lógica principal de carga
├── main.py               # Punto de entrada CLI
│
└── auth_ml.py            # Script de autenticación ML
```

## Flujo de Trabajo

1. **Preparar datos** en Google Sheet (productos con status `pending`)
2. **Subir imágenes** a Google Drive y compartir con service account
3. **Copiar IDs** de imágenes al Sheet
4. **Ejecutar** `python main.py`

