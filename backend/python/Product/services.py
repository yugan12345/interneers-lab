from .repositories import ProductRepository
from .validators import validate_product_data


class ProductService:
    """
    Service layer — owns all business logic for the Product domain.

    Sits between the Controller (HTTP) and Repository (storage).
    Responsible for:
      - Validating incoming data before any storage operation
      - Enforcing business rules (e.g. product must exist before update)
      - Pagination logic
      - Coordinating between validators and the Repository

    Never sends HTTP responses (that is the Controller's job).
    Never touches storage directly (that is the Repository's job).

    Accepts a repository via constructor injection (Dependency Injection)
    so that tests can pass a FakeRepository instead of hitting real storage.
    """

    def __init__(self, repository: ProductRepository = None):
        # Dependency Injection — defaults to real repository in production,
        # but allows a fake/mock repository to be injected during testing.
        self.repository = repository or ProductRepository()

    def create_product(self, data: dict) -> dict:
        """
        Validates all required fields then delegates creation to the Repository.
        Returns the created product as a dict, or an error dict on failure.
        """
        errors = validate_product_data(data, require_all_fields=True)
        if errors:
            return {"error": "Validation failed", "details": errors}

        product = self.repository.create(data)
        return {"product": product.to_dict()}

    def get_product(self, product_id: str) -> dict:
        """
        Fetches a single product by ID.
        Returns an error dict if the product does not exist.
        """
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}

        return {"product": product.to_dict()}

    def get_all_products(self, page: int, page_size: int) -> dict:
        """
        Fetches all products with pagination applied.

        Pagination logic lives here in the Service — NOT in the Controller
        or Repository — because deciding how to slice data is a business rule.
        """
        all_products = self.repository.get_all()
        total_products = len(all_products)
        total_pages = max(1, (total_products + page_size - 1) // page_size)

        if page > total_pages and total_products > 0:
            return {
                "error": f"Page {page} does not exist. Only {total_pages} page(s) available."
            }

        start = (page - 1) * page_size
        end = start + page_size

        return {
            "page": page,
            "page_size": page_size,
            "total_products": total_products,
            "total_pages": total_pages,
            "products": [p.to_dict() for p in all_products[start:end]],
        }

    def full_update_product(self, product_id: str, data: dict) -> dict:
        """
        Handles full update — all fields must be present.
        Validates existence first, then validates all fields before updating.
        """
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}

        errors = validate_product_data(data, require_all_fields=True)
        if errors:
            return {"error": "Validation failed", "details": errors}

        updated = self.repository.update(product, data)
        return {"product": updated.to_dict()}

    def partial_update_product(self, product_id: str, data: dict) -> dict:
        """
        Handles partial update — only provided fields are updated.
        Validates existence first, rejects empty body, then validates
        only the fields that were actually sent.
        """
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}

        if not data:
            return {"error": "Provide at least one field to update."}

        errors = validate_product_data(data, require_all_fields=False)
        if errors:
            return {"error": "Validation failed", "details": errors}

        updated = self.repository.update(product, data)
        return {"product": updated.to_dict()}

    def delete_product(self, product_id: str) -> dict:
        """
        Verifies the product exists before delegating deletion to the Repository.
        Returns an empty dict on success — the Controller returns 204 No Content.
        """
        product = self.repository.get_by_id(product_id)
        if not product:
            return {"error": "Product not found"}

        self.repository.delete(product)
        return {}
