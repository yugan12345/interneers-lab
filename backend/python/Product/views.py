import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .services import ProductService

# Single shared service instance — safe to reuse across requests
# as the Service layer holds no request-specific state.
service = ProductService()

PAGE_SIZE = 2  # default number of products returned per page


@method_decorator(csrf_exempt, name="dispatch")
class ProductListView(View):
    """
    Controller for collection-level Product endpoints.

    Handles:
      GET  /products/  — list all products (paginated)
      POST /products/  — create a new product

    Controller responsibilities only:
      - Parse and validate HTTP request format (JSON body, query params)
      - Delegate all business logic to ProductService
      - Map service results to appropriate HTTP responses

    Does NOT: validate business rules, access storage, or handle pagination.
    """

    def get(self, request):
        """
        Returns a paginated list of products.
        Query params: ?page=1&page_size=10

        Only HTTP-level parsing happens here (is page a valid integer?).
        Pagination logic itself lives in the Service layer.
        """
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

        result = service.get_all_products(page, page_size)

        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=400)

        return JsonResponse(result, status=200)

    def post(self, request):
        """
        Creates a new product.
        Only validates that the request body is valid JSON and a dict.
        All field-level validation is delegated to the Service layer.
        """
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
                    "message": "Request body must be a JSON object",
                },
                status=400,
            )

        result = service.create_product(data)

        if "error" in result:
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=400,
            )

        return JsonResponse(
            {"message": "Product created successfully", "product": result["product"]},
            status=201,
        )


@method_decorator(csrf_exempt, name="dispatch")
class ProductDetailView(View):
    """
    Controller for single-resource Product endpoints.

    Handles:
      GET    /products/<id>/  — fetch one product
      PUT    /products/<id>/  — full update (all fields required)
      PATCH  /products/<id>/  — partial update (only send changed fields)
      DELETE /products/<id>/  — delete a product
    """

    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get(self, request, product_id):
        """Fetches a single product by its ID."""
        result = service.get_product(str(product_id))

        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=404)

        return JsonResponse(result["product"], status=200)

    def put(self, request, product_id):
        """
        Full update — all fields must be provided.
        The Service enforces require_all_fields=True validation.
        """
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
            return JsonResponse({"error": "Invalid request body"}, status=400)

        result = service.full_update_product(str(product_id), data)

        if "error" in result:
            status = 404 if result["error"] == "Product not found" else 400
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=status,
            )

        return JsonResponse(
            {
                "message": "Product fully updated successfully",
                "product": result["product"],
            },
            status=200,
        )

    def patch(self, request, product_id):
        """
        Partial update — only send the fields you want to change.
        The Service enforces require_all_fields=False validation,
        meaning only the provided fields are checked.
        """
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
            return JsonResponse({"error": "Invalid request body"}, status=400)

        result = service.partial_update_product(str(product_id), data)

        if "error" in result:
            status = 404 if result["error"] == "Product not found" else 400
            return JsonResponse(
                {"error": result["error"], "details": result.get("details", {})},
                status=status,
            )

        return JsonResponse(
            {
                "message": "Product partially updated successfully",
                "product": result["product"],
            },
            status=200,
        )

    def delete(self, request, product_id):
        """
        Deletes a product.
        Returns 204 No Content on success — standard REST convention
        for DELETE (no response body needed).
        """
        result = service.delete_product(str(product_id))

        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=404)

        return HttpResponse(status=204)
