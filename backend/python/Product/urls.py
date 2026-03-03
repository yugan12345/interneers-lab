from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path("products/", ProductListView.as_view()),  # GET all, POST new
    path(
        "products/<int:product_id>/", ProductDetailView.as_view()
    ),  # GET one, PUT, DELETE
]
