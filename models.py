from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Product:
    title: str
    category_id: str
    price: float
    currency_id: str = "ARS"
    available_quantity: int = 1
    buying_mode: str = "buy_it_now"
    condition: str = "new"
    listing_type_id: str = "gold_special"
    description: str = ""
    images_ids: List[str] = field(default_factory=list)  # IDs de Drive
    video_id: Optional[str] = None
    attributes: List[dict] = field(default_factory=list)
    shipping_free: bool = False
    
    # Campos de control
    row_number: int = 0
    ml_id: Optional[str] = None
    status: str = "pending"  # pending, processing, success, error
    error_message: Optional[str] = None

    @classmethod
    def from_sheet_row(cls, row: List[str], row_number: int) -> 'Product':
        """Crea un Product desde una fila del sheet"""
        return cls(
            title=row[0] if len(row) > 0 else "",
            category_id=row[1] if len(row) > 1 else "",
            price=float(row[2]) if len(row) > 2 and row[2] else 0,
            available_quantity=int(row[3]) if len(row) > 3 and row[3] else 1,
            condition=row[4] if len(row) > 4 and row[4] else "new",
            listing_type_id=row[5] if len(row) > 5 and row[5] else "gold_special",
            description=row[6] if len(row) > 6 else "",
            images_ids=row[7].split(',') if len(row) > 7 and row[7] else [],
            shipping_free=row[8].lower() == 'true' if len(row) > 8 and row[8] else False,
            row_number=row_number
        )
    
    def to_ml_payload(self, uploaded_images: List[str]) -> dict:
        """Convierte el producto al formato de ML API"""
        payload = {
            "title": self.title,
            "category_id": self.category_id,
            "price": self.price,
            "currency_id": self.currency_id,
            "available_quantity": self.available_quantity,
            "buying_mode": self.buying_mode,
            "condition": self.condition,
            "listing_type_id": self.listing_type_id,
            "pictures": [{"source": url} for url in uploaded_images]
        }
        
        if self.description:
            payload["description"] = {"plain_text": self.description}
        
        if self.shipping_free:
            payload["shipping"] = {
                "mode": "me2",
                "free_shipping": True
            }
        
        if self.attributes:
            payload["attributes"] = self.attributes
            
        return payload