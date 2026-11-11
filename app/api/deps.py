from app.services.product_service import ProductService
_product_service = ProductService()

def get_product_service() -> ProductService:
    return _product_service
