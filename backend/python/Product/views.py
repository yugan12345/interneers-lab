import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .validators import validate_product_data

PRODUCTS = {}
NEXT_ID = 1
PAGE_SIZE = 2


@method_decorator(csrf_exempt, name="dispatch")
class ProductListView(View):
    def get(self, request):
        products = list(PRODUCTS.values())
        total_products = len(products)

        try:
            page = int(request.GET.get("page", 1))
            if page < 1:
                raise ValueError
        except ValueError:
            return JsonResponse(
                {
                    "error": "Invalid page number",
                    "message": "page must be a positive integer e.g. ?page=1",
                },
                status=400,
            )

        try:
            page_size = int(request.GET.get("page_size", PAGE_SIZE))
            if page_size < 1:
                raise ValueError
        except ValueError:
            return JsonResponse(
                {
                    "error": "Invalid page_size",
                    "message": "page_size must be a positive integer e.g. ?page_size=5",
                },
                status=400,
            )

        total_pages = max(1, (total_products + page_size - 1) // page_size)

        if page > total_pages and total_products > 0:
            return JsonResponse(
                {
                    "error": "Page out of range",
                    "message": f"Page {page} does not exist. Only {total_pages} page(s) available.",
                },
                status=400,
            )

        start = (page - 1) * page_size
        end = start + page_size

        return JsonResponse(
            {
                "page": page,
                "page_size": page_size,
                "total_products": total_products,
                "total_pages": total_pages,
                "products": products[start:end],
            },
            status=200,
        )

    def post(self, request):
        global NEXT_ID

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "error": "Invalid JSON",
                    "message": "Request body must be valid JSON.",
                },
                status=400,
            )

        if not isinstance(data, dict):
            return JsonResponse(
                {
                    "error": "Invalid request body",
                    "message": 'Request body must be a JSON object e.g. {"name": "iPhone"}',
                },
                status=400,
            )

        errors = validate_product_data(data, require_all_fields=True)
        if errors:
            return JsonResponse(
                {
                    "error": "Validation failed",
                    "message": "One or more fields are invalid.",
                    "details": errors,
                },
                status=400,
            )

        product = {
            "id": NEXT_ID,
            "name": data["name"],
            "description": data["description"],
            "category": data["category"],
            "price": float(data["price"]),
            "brand": data["brand"],
            "quantity": int(data["quantity"]),
        }

        PRODUCTS[NEXT_ID] = product
        NEXT_ID += 1

        return JsonResponse(
            {"message": "Product created successfully", "product": product}, status=201
        )


@method_decorator(csrf_exempt, name="dispatch")
class ProductDetailView(View):
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_product_or_404(self, product_id):
        return PRODUCTS.get(product_id)

    def get(self, request, product_id):
        product = self.get_product_or_404(product_id)
        if not product:
            return JsonResponse(
                {
                    "error": "Product not found",
                    "message": f"No product exists with ID {product_id}.",
                },
                status=404,
            )
        return JsonResponse(product, status=200)

    def put(self, request, product_id):
        """All fields required"""
        product = self.get_product_or_404(product_id)
        if not product:
            return JsonResponse(
                {
                    "error": "Product not found",
                    "message": f"No product exists with ID {product_id}. Cannot update.",
                },
                status=404,
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "error": "Invalid JSON",
                    "message": "Request body must be valid JSON.",
                },
                status=400,
            )

        if not isinstance(data, dict):
            return JsonResponse(
                {
                    "error": "Invalid request body",
                    "message": 'Request body must be a JSON object e.g. {"name": "iPhone"}',
                },
                status=400,
            )

        errors = validate_product_data(data, require_all_fields=True)
        if errors:
            return JsonResponse(
                {
                    "error": "Validation failed",
                    "message": "All fields are required for a full update.",
                    "details": errors,
                },
                status=400,
            )

        product = {
            "id": product_id,
            "name": data["name"],
            "description": data["description"],
            "category": data["category"],
            "price": float(data["price"]),
            "brand": data["brand"],
            "quantity": int(data["quantity"]),
        }

        PRODUCTS[product_id] = product
        return JsonResponse(
            {"message": "Product fully updated successfully", "product": product},
            status=200,
        )

    def patch(self, request, product_id):
        """Partial update — only send fields you want to change"""
        product = self.get_product_or_404(product_id)
        if not product:
            return JsonResponse(
                {
                    "error": "Product not found",
                    "message": f"No product exists with ID {product_id}. Cannot update.",
                },
                status=404,
            )

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "error": "Invalid JSON",
                    "message": "Request body must be valid JSON.",
                },
                status=400,
            )
        if not isinstance(data, dict):
            return JsonResponse(
                {
                    "error": "Invalid request body",
                    "message": 'Request body must be a JSON object e.g. {"name": "iPhone"}',
                },
                status=400,
            )
        if not data:
            return JsonResponse(
                {
                    "error": "Empty request body",
                    "message": "Provide at least one field to update.",
                },
                status=400,
            )

        errors = validate_product_data(data, require_all_fields=False)
        if errors:
            return JsonResponse(
                {
                    "error": "Validation failed",
                    "message": "One or more fields are invalid.",
                    "details": errors,
                },
                status=400,
            )

        if "name" in data:
            product["name"] = data["name"]
        if "description" in data:
            product["description"] = data["description"]
        if "category" in data:
            product["category"] = data["category"]
        if "price" in data:
            product["price"] = float(data["price"])
        if "brand" in data:
            product["brand"] = data["brand"]
        if "quantity" in data:
            product["quantity"] = int(data["quantity"])

        PRODUCTS[product_id] = product
        return JsonResponse(
            {"message": "Product partially updated successfully", "product": product},
            status=200,
        )

    def delete(self, request, product_id):
        product = self.get_product_or_404(product_id)
        if not product:
            return JsonResponse(
                {
                    "error": "Product not found",
                    "message": f"No product exists with ID {product_id}. Cannot delete.",
                },
                status=404,
            )

        del PRODUCTS[product_id]
        return HttpResponse(status=204)
