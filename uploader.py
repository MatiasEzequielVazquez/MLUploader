import os
import tempfile
from typing import List
from models import Product
from google_client import GoogleClient
from validators import ProductValidator

class BulkUploader:
    def __init__(self, dry_run=False):
        self.google_client = GoogleClient()
        self.validator = ProductValidator()
        self.dry_run = dry_run
        
        # Solo importar ML client si no es dry-run
        if not dry_run:
            from ml_client import MLClient
            self.ml_client = MLClient()
        else:
            self.ml_client = None
            print("Modo DRY-RUN activado - No se publicarán productos reales\n")
        
    def process_batch(self) -> dict:
        """Procesa un batch de productos"""
        products = self.google_client.get_pending_products()
        
        results = {
            'total': len(products),
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
        print(f"\nProcesando {results['total']} productos...\n")
        
        for product in products:
            print(f"[{product.row_number}] {product.title}")
            
            # Validar
            is_valid, errors = self.validator.validate(product)
            if not is_valid:
                product.status = "error"
                product.error_message = "; ".join(errors)
                self.google_client.update_product_status(product)
                print(f"  ✗ Validación fallida: {product.error_message}")
                results['failed'] += 1
                continue
            
            # Actualizar status a processing
            product.status = "processing"
            self.google_client.update_product_status(product)
            
            if self.dry_run:
                # MODO SIMULACIÓN
                print(f"  [DRY-RUN] Simulando subida...")
                print(f"     - Título: {product.title[:50]}...")
                print(f"     - Precio: ${product.price}")
                print(f"     - Categoría: {product.category_id}")
                
                # Simular imágenes
                if product.images_ids:
                    print(f"     - Imágenes: {len(product.images_ids)} archivos")
                
                # Simular éxito
                product.status = "simulated"
                product.ml_id = f"MLA-SIMULATED-{product.row_number}"
                print(f"  ✓ [DRY-RUN] Simulado exitosamente: {product.ml_id}")
                results['success'] += 1
            else:
                # MODO REAL
                # Descargar y subir imágenes
                uploaded_images = self._process_images(product)
                if not uploaded_images:
                    product.status = "error"
                    product.error_message = "Error procesando imágenes"
                    self.google_client.update_product_status(product)
                    results['failed'] += 1
                    continue
                
                # Crear publicación
                payload = product.to_ml_payload(uploaded_images)
                success, ml_id, error = self.ml_client.create_listing(payload)
                
                if success:
                    product.status = "success"
                    product.ml_id = ml_id
                    print(f"  ✓ Publicado: {ml_id}")
                    results['success'] += 1
                else:
                    product.status = "error"
                    product.error_message = error
                    print(f"  ✗ Error: {error}")
                    results['failed'] += 1
            
            self.google_client.update_product_status(product)
        
        return results
    
    def _process_images(self, product: Product) -> List[str]:
        """Descarga imágenes de Drive y las sube a ML"""
        if self.dry_run:
            # En dry-run, simular URLs de imágenes
            return [f"https://simulated-image-{i}.jpg" for i in range(len(product.images_ids))]
        
        uploaded_urls = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            for idx, image_id in enumerate(product.images_ids):
                image_id = image_id.strip()
                
                # Descargar de Drive
                tmp_path = os.path.join(tmpdir, f"img_{idx}.jpg")
                if not self.google_client.download_image(image_id, tmp_path):
                    continue
                
                # Subir a ML
                url = self.ml_client.upload_image(tmp_path)
                if url:
                    uploaded_urls.append(url)
        
        return uploaded_urls