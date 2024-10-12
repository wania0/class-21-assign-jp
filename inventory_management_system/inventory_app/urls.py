from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.get_categories_or_create_category),
    path("categories/<int:id>/", views.get_or_update_or_delete_category),
    path("suppliers/", views.get_suppliers_or_create_supplier),
    path("suppliers/<int:id>/", views.get_or_update_or_delete_supplier),
    path("products/", views.get_products_or_create_product),
    path("products/<int:id>/", views.get_or_update_or_delete_product),

]