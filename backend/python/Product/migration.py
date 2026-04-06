"""
Migration script: Week 3 → Week 4

Problem:
  Before Week 4, Product.category was a StringField storing a plain text
  category name (e.g. "Electronics"). After Week 4, it is a ReferenceField
  pointing to a ProductCategory document.

  Existing products in MongoDB have a string value in their 'category' field.
  MongoEngine will now expect an ObjectId there instead. Without migration,
  those products will either error on load or silently drop the category value.

Strategy:
  1. For each unique category string found in existing products, create a
     ProductCategory document with that string as its title.
  2. Update every product that had that string to instead reference the new
     ProductCategory document.
  3. Products with no category string (null/empty) are left with category=None.

Run this script ONCE after deploying the Week 4 code, before starting the server:
  python manage.py shell < Product/migration.py

Or run it as a standalone Django management command if you prefer.
"""

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()

from datetime import datetime, timezone
from mongoengine import connect
from mongoengine.connection import get_db


def run_migration():
    db = get_db()
    products_collection = db["products"]
    categories_collection = db["product_categories"]

    now = datetime.now(timezone.utc)
    existing_strings = products_collection.distinct("category")
    existing_strings = [c for c in existing_strings if c and isinstance(c, str)]

    print(
        f"Found {len(existing_strings)} unique category string(s): {existing_strings}"
    )

    # Step 2: Create a ProductCategory document for each unique string
    string_to_id = {}
    for category_string in existing_strings:
        # Check if a category with this title already exists (idempotent re-runs)
        existing = categories_collection.find_one({"title": category_string})
        if existing:
            string_to_id[category_string] = existing["_id"]
            print(f"  Category '{category_string}' already exists — skipping creation")
        else:
            result = categories_collection.insert_one(
                {
                    "title": category_string,
                    "description": f"Auto-migrated from legacy category string: '{category_string}'",
                    "created_at": now,
                    "updated_at": now,
                }
            )
            string_to_id[category_string] = result.inserted_id
            print(
                f"  Created category '{category_string}' with id {result.inserted_id}"
            )

    # Step 3: Update all products to use the ObjectId reference instead of the string
    total_updated = 0
    for category_string, category_id in string_to_id.items():
        result = products_collection.update_many(
            {"category": category_string}, {"$set": {"category": category_id}}
        )
        print(
            f"  Updated {result.modified_count} product(s) from '{category_string}' → ObjectId({category_id})"
        )
        total_updated += result.modified_count

    # Step 4: Null out any remaining products with no category or invalid references
    null_result = products_collection.update_many(
        {"category": {"$type": "string"}},  # catch any remaining string values
        {"$set": {"category": None}},
    )
    if null_result.modified_count:
        print(
            f"  Nullified {null_result.modified_count} product(s) with unresolvable category strings"
        )

    print(f"\nMigration complete. {total_updated} product(s) updated total.")

run_migration()
