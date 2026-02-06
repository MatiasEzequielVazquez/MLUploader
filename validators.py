from models import Product
from typing import List, Tuple

class ProductValidator:
    @staticmethod
    def validate(product: Product) -> Tuple[bool, List[str]]:
        """
        Valida un producto antes de subirlo
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        
        # Título
        if not product.title or len(product.title) < 10:
            errors.append("El título debe tener al menos 10 caracteres")
        if len(product.title) > 60:
            errors.append("El título no puede superar los 60 caracteres")
        
        # Precio
        if product.price <= 0:
            errors.append("El precio debe ser mayor a 0")
        
        # Categoría
        if not product.category_id:
            errors.append("Debe especificar una categoría")
        
        # Stock
        if product.available_quantity < 0:
            errors.append("El stock no puede ser negativo")
        
        # Imágenes
        #if not product.images_ids:
        #    errors.append("Debe incluir al menos una imagen")
        if len(product.images_ids) > 12:
            errors.append("No se pueden subir más de 12 imágenes")
        
        # Condición
        if product.condition not in ['new', 'used', 'not_specified']:
            errors.append("Condición inválida (new, used, not_specified)")
        
        return len(errors) == 0, errors