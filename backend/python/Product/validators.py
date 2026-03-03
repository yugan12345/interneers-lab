from django.core.exceptions import ValidationError


def validate_product_data(data, require_all_fields=True):
    """
    Validates incoming product data.
    - require_all_fields=True  → used when creating a product (all fields must be present)
    - require_all_fields=False → used when updating a product (only sent fields are checked)
    """
    errors = {}

    # If creating, these fields are mandatory
    if require_all_fields:
        required_fields = [
            "name",
            "description",
            "category",
            "price",
            "brand",
            "quantity",
        ]
        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                errors[field] = f"{field} is required"

    # Validate price if provided
    if "price" in data:
        try:
            price = float(data["price"])
            if price < 0:
                errors["price"] = "Price must be a positive number"
        except (ValueError, TypeError):
            errors["price"] = "Price must be a valid number"

    # Validate quantity if provided
    if "quantity" in data:
        try:
            quantity = int(data["quantity"])
            if quantity < 0:
                errors["quantity"] = "Quantity must be a positive integer"
        except (ValueError, TypeError):
            errors["quantity"] = "Quantity must be a valid integer"

    # Validate name length if provided
    if "name" in data and data["name"]:
        if len(data["name"]) > 255:
            errors["name"] = "Name must be under 255 characters"

    return errors
