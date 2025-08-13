from pydantic import BaseModel

class Product(BaseModel):
    product_id: str        # stable identifier (e.g., UPC or slug)
    name: str              # product title
    price: float | None    # price can be missing on some pages
    in_stock: bool         # True/False from availability text
    url: str               # canonical product URL
