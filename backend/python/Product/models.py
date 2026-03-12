from django.db import models
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField
from datetime import datetime, timezone

"""
    Domain model representing a Product in the inventory system.

    Inherits from MongoEngine's Document class which maps this
    Python class directly to the 'products' collection in MongoDB.
    No separate ORM mapper file is needed (unlike SQLAlchemy)
    because MongoDB's document structure mirrors Python dicts naturally.

    Fields are defined as MongoEngine field types which handle
    both type enforcement and MongoDB serialization automatically.
"""

class Product(Document):
    name = StringField(required=True, max_length=255)
    description = StringField(required=True)
    category = StringField(required=True)
    price = FloatField(required=True, min_value=0.01)
    brand = StringField(required=True)
    quantity = IntField(required=True, min_value=1)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    # Audit fields — automatically set on create, updated_at
    # is refreshed on every update via the Repository layer.
    # No migration needed to add these — MongoDB is schemaless.

    meta = {"collection": "products"}

    def to_dict(self):
        """
        Serializes the MongoEngine Document into a plain Python dict.

        Required because JsonResponse cannot serialize MongoEngine
        objects directly. The MongoDB ObjectId is converted to a
        string since ObjectId is not JSON serializable by default.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }