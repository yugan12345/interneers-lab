from .models import Product
from datetime import datetime, timezone

"""
    Repository layer — the only layer that directly interacts with
    the persistence store.

    Follows the Repository Pattern: abstracts all storage logic behind
    a clean interface so the Service layer never needs to know HOW
    or WHERE data is stored.

    Benefit: swapping the underlying storage technology only requires
    changes to this file. The Service and Controller layers remain
    completely untouched.

    Method names use data operation language (create, get, update, delete)
    NOT HTTP verbs — the Repository has no knowledge that HTTP even exists.
"""


class ProductRepository:
    def create(self, data: dict) -> Product:
        """
        Persists a new Product to the store.
        Returns the saved Product object with its auto-generated ID.
        """
        product = Product(
            name=data["name"],
            description=data["description"],
            category=data["category"],
            price=float(data["price"]),
            brand=data["brand"],
            quantity=int(data["quantity"]),
        )
        product.save()
        return product

    def get_by_id(self, product_id: str) -> Product | None:
        """
        Fetches a single Product by its ID.
        Returns None if the product does not exist or the ID is invalid.
        Callers must always handle the None case.
        """
        try:
            return Product.objects.get(id=product_id)
        except (Product.DoesNotExist, Exception):
            return None

    def get_all(self) -> list:
        """
        Fetches all Products from the store as a Python list.
        Pagination is intentionally NOT handled here — that is the
        responsibility of the Service layer.
        """
        return list(Product.objects.all())

    def update(self, product: Product, data: dict) -> Product:
        """
        Applies updates to an existing Product and persists the changes.

        Handles both full updates (all fields) and partial updates (subset
        of fields) — the distinction is made upstream in the Service layer.
        Only fields present in `data` are modified, leaving others unchanged.

        Always refreshes updated_at to the current UTC time on every save.
        """
        for field in ["name", "description", "category", "brand"]:
            if field in data:
                setattr(product, field, data[field])
        if "price" in data:
            product.price = float(data["price"])
        if "quantity" in data:
            product.quantity = int(data["quantity"])

        product.updated_at = datetime.now(timezone.utc)
        product.save()
        return product

    def delete(self, product: Product) -> None:
        """
        Permanently removes a Product from the store.
        Existence is verified upstream in the Service layer
        before this method is called.
        """
        product.delete()
