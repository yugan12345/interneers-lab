# django_app/urls.py

from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

from Product.views import ProductListView, ProductDetailView


def hello_name(request):
    """
    A simple view that returns 'Hello, {name}' in JSON format.
    Uses a query parameter named 'name'.
    """
    # Get 'name' from the query string, default to 'World' if missing
    name = request.GET.get("name", "World")
    return JsonResponse({"message": f"Hello, {name}!"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", hello_name),
    path("products/", ProductListView.as_view()),  # GET all, POST new
    path(
        "products/<int:product_id>/", ProductDetailView.as_view()
    ),  # GET one, PUT, DELETE
    # Example usage: /hello/?name=Bob
    # returns {"message": "Hello, Bob!"}
]
