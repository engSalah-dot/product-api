

from itertools import product

from app.schemas.product import ProductRead
from app.schemas.product import ProductCreate
from datetime import datetime, timezone
import logging
from app.schemas.product import ProductRead

logger = logging.getLogger(__name__)
class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found.")

class ProductService:
    def __init__(self)-> None:
        self._products :dict[int,ProductRead] = {}
        self._next_id = 1
        

    def create_product(self, data: ProductCreate) -> ProductRead: 
        now=datetime.now(timezone.utc)
        product = ProductRead(
            id=self._next_id,
            created_at=now,
            updated_at=now,
            **data.model_dump(),
        )
        self._products[product.id] = product
        self._next_id += 1
        logging.info(f"Product created: {product}")
        return product
    def get_product(self, product_id: int) -> ProductRead:
        product = self._products.get(product_id)
        if not product:
            logging.error(f"Product with ID {product_id} not found.")
            raise ProductNotFoundError(product_id)
        logging.info(f"Product retrieved: {product}")
        return product
    def list (self,skip:int=0,limit:int=10)->list[ProductRead]:
        products=list(self._products.values())[skip:skip+limit]
        logging.info(f"Products listed: {products}")
        return products
    def update_product(self, product_id: int, data: ProductCreate) -> ProductRead:
        product=self.get_product(product_id)
        changes=data.model_dump(exclude_unset=True)
        updated = product.model_copy(update={**changes, "updated_at": datetime.now(timezone.utc)})
                
        self._products[product_id]=updated
        logging.info(f"Product updated: {updated}")
        return updated
    
    def delete_product(self, product_id: int) -> None:
        self.get_product(product_id)
        del self._products[product_id]
        logging.info(f"Product with ID {product_id} deleted.")
        
      