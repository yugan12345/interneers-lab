from django.core.exceptions import ValidationError


def validate_product_data(data, require_all_fields=True):
    errors = {}

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

    if "price" in data:
        if data["price"] in [None, ""]:
            errors["price"] = "Price cannot be null or empty"
        else:
            try:
                price = float(data["price"])
                if price <= 0:
                    errors["price"] = "Price must be a positive non-zero number"
            except (ValueError, TypeError):
                errors["price"] = "Price must be a valid number"

    if "quantity" in data:
        if data["quantity"] in [None, ""]:
            errors["quantity"] = "Quantity cannot be null or empty"
        else:
            try:
                quantity = int(data["quantity"])
                if quantity <= 0:
                    errors["quantity"] = "Quantity must be a positive non-zero integer"
            except (ValueError, TypeError):
                errors["quantity"] = "Quantity must be a valid integer"

    if "name" in data and data["name"]:
        if len(data["name"]) > 255:
            errors["name"] = "Name must be under 255 characters"

    return errors
