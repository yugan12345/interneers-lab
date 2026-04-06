from mongoengine import (
    Document,
    StringField,
    FloatField,
    IntField,
    DateTimeField,
    ReferenceField,
    LazyReferenceField,
)

"""
    Domain models for the inventory system.

    Week 4 changes:
      - ProductCategory is a new first-class entity with its own collection.
      - Product.category is now a ReferenceField to ProductCategory instead
        of a plain StringField. This creates a real relationship between the
        two documents in MongoDB, similar to a foreign key in SQL.
      - Migration note: existing products with a string category field will
        have a null category reference after this change. The migration script
        (migration.py) handles backfilling these to a default category.
"""


class ProductCategory(Document):
    """
    Represents a product category in the inventory system.

    Examples: "Food", "Electronics", "Kitchen Essentials", "Toys"

    Stored in the 'product_categories' collection. Products reference
    this document via a ReferenceField, so changing a category's title
    is automatically reflected everywhere without updating Product docs.
    """

    title = StringField(required=True, max_length=255)
    description = StringField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    meta = {"collection": "product_categories"}

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class Product(Document):
    """
    Represents a product in the warehouse inventory.

    Week 4: category is now a ReferenceField to ProductCategory.
    MongoEngine stores the ObjectId of the category document in the
    'category' field of each product document in MongoDB. When accessed,
    MongoEngine automatically fetches the referenced category document.
    """

    name = StringField(required=True, max_length=255)
    description = StringField(required=True)
    # ReferenceField stores the ObjectId of the related ProductCategory.
    # reverse_delete_rule=mongoengine.NULLIFY would nullify this field
    # if the category is deleted — we handle this in the service layer instead
    # to give more control and clearer error messages.
    category = ReferenceField(ProductCategory, required=False)
    price = FloatField(required=True)
    brand = StringField(required=True)
    quantity = IntField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField(required=True)

    meta = {"collection": "products"}

    def __str__(self):
        return f"{self.name} ({self.brand})"

    def to_dict(self):
        """
        Serializes the Product to a plain dict.

        The category field is either serialized as a nested dict (if the
        referenced document is loaded) or as just its ID string (if not loaded).
        This handles both the case where category is populated and where it is None
        (for products created before Week 4 that have no category assigned).
        """
        category_data = None
        if self.category:
            try:
                # Access the referenced document — triggers a DB fetch if not cached
                category_data = {
                    "id": str(self.category.id),
                    "title": self.category.title,
                }
            except Exception:
                # Category reference exists but document was deleted
                category_data = {"id": str(self.category.id), "title": None}

        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": category_data,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
