from .models import Product, ProductCategory
from datetime import datetime, timezone
from mongoengine.errors import InvalidQueryError, ValidationError as MongoValidationError

"""
    Repository layer — the only layer that directly interacts with MongoDB.
"""


class ProductCategoryRepository:
    def create(self, data: dict) -> ProductCategory:
        now = datetime.now(timezone.utc)
        category = ProductCategory(
            title=data["title"],
            description=data["description"],
            created_at=now,
            updated_at=now,
        )
        category.save()
        return category

    def get_by_id(self, category_id: str) -> ProductCategory | None:
        try:
            return ProductCategory.objects.get(id=category_id)
        except ProductCategory.DoesNotExist:
            return None
        except (InvalidQueryError, MongoValidationError, Exception):
            return None

    def get_all(self) -> list:
        return list(ProductCategory.objects.all())

    def count(self) -> int:
        # Categories have no filters — plain count
        return ProductCategory.objects.count()

    def get_paginated(self, skip: int, limit: int) -> list:
        return list(ProductCategory.objects.skip(skip).limit(limit))

    def update(self, category: ProductCategory, data: dict) -> ProductCategory:
        if "title" in data:
            category.title = data["title"]
        if "description" in data:
            category.description = data["description"]
        category.updated_at = datetime.now(timezone.utc)
        category.save()
        return category

    def delete(self, category: ProductCategory) -> None:
        category.delete()


class ProductRepository:
    def create(self, data: dict, category: ProductCategory | None = None) -> Product:
        now = datetime.now(timezone.utc)
        product = Product(
            name=data["name"],
            description=data["description"],
            category=category,
            price=float(data["price"]),
            brand=data["brand"],
            quantity=int(data["quantity"]),
            created_at=now,
            updated_at=now,
        )
        product.save()
        return product

    def get_by_id(self, product_id: str) -> Product | None:
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None
        except (InvalidQueryError, MongoValidationError, Exception):
            return None

    def count(self, filters: dict = None) -> int:
        """
        Returns product count, optionally with DB-side filters applied.
        filters is a dict of MongoEngine query kwargs e.g. {"brand": "Apple", "price__gte": 100}
        """
        qs = Product.objects
        if filters:
            qs = qs.filter(**filters)
        return qs.count()

    def get_paginated(self, skip: int, limit: int, filters: dict = None) -> list:
        """
        Fetches a page of products using DB-side skip/limit with optional filters.
        Both count() and get_paginated() must always receive the same filters
        so pagination totals match the actual results returned.
        """
        qs = Product.objects
        if filters:
            qs = qs.filter(**filters)
        return list(qs.skip(skip).limit(limit))

    def get_by_category(self, category: ProductCategory) -> list:
        return list(Product.objects.filter(category=category))

    def count_by_category(self, category: ProductCategory) -> int:
        return Product.objects.filter(category=category).count()

    def update(self, product: Product, data: dict, category=False) -> Product:
        for field in ["name", "description", "brand"]:
            if field in data:
                setattr(product, field, data[field])
        if "price" in data:
            product.price = float(data["price"])
        if "quantity" in data:
            product.quantity = int(data["quantity"])
        if category is not False:
            product.category = category
        product.updated_at = datetime.now(timezone.utc)
        product.save()
        return product

    def set_category(self, product: Product, category: ProductCategory) -> Product:
        product.category = category
        product.updated_at = datetime.now(timezone.utc)
        product.save()
        return product

    def remove_category(self, product: Product) -> Product:
        product.category = None
        product.updated_at = datetime.now(timezone.utc)
        product.save()
        return product

    def bulk_create(self, products: list) -> list:
        now = datetime.now(timezone.utc)
        product_objects = [
            Product(
                name=p["name"],
                description=p["description"],
                category=p.get("category"),
                price=float(p["price"]),
                brand=p["brand"],
                quantity=int(p["quantity"]),
                created_at=now,
                updated_at=now,
            )
            for p in products
        ]
        Product.objects.insert(product_objects, load_bulk=False)
        return product_objects

    def delete(self, product: Product) -> None:
        product.delete()