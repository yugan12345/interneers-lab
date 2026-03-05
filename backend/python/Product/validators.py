def validate_product_data(data, require_all_fields=True):
    """
    Validates product data for create (POST/PUT) and partial update (PATCH).
    When require_all_fields=True, all fields must be present.
    When require_all_fields=False, only provided fields are validated.
    Returns a dict of field-level errors, empty if all validations pass.
    """
    errors = {}

    # Enforce all fields on create and full update
    if require_all_fields:
        required_fields = ["name", "description", "category", "price", "brand", "quantity"]
        for field in required_fields:
            if field not in data or data[field] in [None, ""]:
                errors[field] = f"{field} is required"

    # Must be a positive non-zero number, rejects booleans and non-numeric values
    if "price" in data and "price" not in errors:
        if data["price"] in [None, ""]:
            errors["price"] = "Price cannot be null or empty"
        elif isinstance(data["price"], bool):
            errors["price"] = "Price must be a valid number"
        else:
            try:
                price = float(data["price"])
                if price <= 0:
                    errors["price"] = "Price must be a positive non-zero number"
            except (ValueError, TypeError):
                errors["price"] = "Price must be a valid number"

    # Must be a positive non-zero integer, bool excluded as it subclasses int in Python
    if "quantity" in data and "quantity" not in errors:
        if data["quantity"] in [None, ""]:
            errors["quantity"] = "Quantity cannot be null or empty"
        elif not isinstance(data["quantity"], int) or isinstance(data["quantity"], bool):
            errors["quantity"] = "Quantity must be a valid integer"
        elif data["quantity"] <= 0:
            errors["quantity"] = "Quantity must be a positive non-zero integer"

    # Must be a non-empty string under 255 characters
    if "name" in data and "name" not in errors:
        if data["name"] in [None, ""]:
            errors["name"] = "Name cannot be null or empty"
        elif not isinstance(data["name"], str):
            errors["name"] = "Name must be a string"
        elif len(data["name"]) > 255:
            errors["name"] = "Name must be under 255 characters"

    # Must be a non-empty string
    if "description" in data and "description" not in errors:
        if data["description"] in [None, ""]:
            errors["description"] = "Description cannot be null or empty"
        elif not isinstance(data["description"], str):
            errors["description"] = "Description must be a string"

    # Must be a non-empty string
    if "category" in data and "category" not in errors:
        if data["category"] in [None, ""]:
            errors["category"] = "Category cannot be null or empty"
        elif not isinstance(data["category"], str):
            errors["category"] = "Category must be a string"

    # Must be a non-empty string
    if "brand" in data and "brand" not in errors:
        if data["brand"] in [None, ""]:
            errors["brand"] = "Brand cannot be null or empty"
        elif not isinstance(data["brand"], str):
            errors["brand"] = "Brand must be a string"

    return errors