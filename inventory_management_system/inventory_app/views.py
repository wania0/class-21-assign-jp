from django.shortcuts import render

# Create your views here.

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Category as category_model
from .models import Supplier as supplier_model
from .models import Product as product_model

from .serializers import CategorySerializer
from .serializers import SupplierSerializer
from .serializers import ProductSerializer


# category
@api_view(['GET', 'POST'])
def get_categories_or_create_category(request: Request):
    data = []
    if request.method == 'GET':
        params = request.query_params
    
        category_objects = category_model.objects
        if params.get("name") is not None:
            category_objects = category_objects.filter(name=params.get("name"))

        if params.get("id") is not None:
            category_objects = category_objects.filter(id=params.get("id"))

        categories = category_objects.all()
    
        serializer = CategorySerializer(categories, many=True)
        data = serializer.data
    
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        
        if serializer.is_valid():
            category_model.objects.create(**serializer.validated_data)
        else:
            return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        data = "category created successfully"
        
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_category(request: Request, id):
    category = category_model.objects.get(pk=id)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=200)

    if request.method == 'PUT':
        serializer = CategorySerializer(data=request.data)
        
        if serializer.is_valid():
             category.name = serializer.validated_data['name']
             category.save()

        else:
            return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        data = "category updated successfully"
        return Response(data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        category.delete()
        data = "deleted"

    return Response(data, status=status.HTTP_200_OK)


# supplier
@api_view(['GET', 'POST'])
def get_suppliers_or_create_supplier(request: Request):
    data = []
    if request.method == 'GET':
        params = request.query_params
        
        supplier_objects = supplier_model.objects
        if params.get("name") is not None:
            supplier_objects = supplier_objects.filter(name=params.get("name"))

        if params.get("id") is not None:
           supplier_objects =supplier_objects.filter(id=params.get("id"))
           
        if params.get("phone_no") is not None:
           supplier_objects =supplier_objects.filter(phone_no=params.get("phone_no"))
           
        suppliers = supplier_objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        data = serializer.data
    
    if request.method == 'POST':
    
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            supplier_model.objects.create(**serializer.validated_data)
        else:
            return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        data = "supplier created successfully"

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_supplier(request: Request, id):
    supplier = supplier_model.objects.get(pk=id)
    
    if request.method == 'GET':
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=200)

    if request.method == 'PUT':
        serializer = SupplierSerializer(data=request.data)
        
        if serializer.is_valid():
             supplier.name = serializer.validated_data['name']
             supplier.phone_no = serializer.validated_data['phone_no']
             supplier.save()

        else:
            return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        data = "supplier updated successfully"
        return Response(data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        supplier.delete()
        data = "deleted"

    return Response(data, status=status.HTTP_200_OK)

# product
@api_view(['GET', 'POST'])
def get_products_or_create_product(request: Request):
    data = []
    if request.method == 'GET':
        params = request.query_params
        
        product_objects = product_model.objects
        if params.get("name") is not None:
            product_objects = product_objects.filter(name=params.get("name"))

        if params.get("id") is not None:
           product_objects =product_objects.filter(id=params.get("id"))
           
        if params.get("cat_id") is not None:
           product_objects =product_objects.filter(cat_id=params.get("cat_id"))
           
        if params.get("supplier_id") is not None:
           product_objects =product_objects.filter(supplier_id=params.get("supplier_id"))
           
        products = product_objects.all()
        serializer = ProductSerializer(products, many=True)
        data = serializer.data
        
    if request.method == 'POST':
        serializer = ProductSerializer(data= request.data)
        category = category_model.objects.get(pk=id)
        if category is None:
            return "category not found"
        if serializer.is_valid():
            product_model.objects.create(**serializer.validated_data)
        else:
            return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        data = "product created successfully"

    return Response(data, status=status.HTTP_200_OK)
        
@api_view(['GET', 'PUT', 'DELETE'])
def get_or_update_or_delete_product(request: Request, id):
    product = product_model.objects.get(pk=id)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=200)

    if request.method == 'PUT':
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
             product.name = serializer.validated_data['name']
             product.cat_id = serializer.validated_data['cat_id']
             product.supplier_id = serializer.validated_data['supplier_id']
             product.save()

        else:
            return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        data = "product updated successfully"
        return Response(data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        product.delete()
        data = "deleted"

    return Response(data, status=status.HTTP_200_OK)



# def total_products():
#     total_products = product_model.objects.count()
#     return total_products


# def total_products_per_category():
#     total_products_per_category= Product.objects.values('cat_id').annotate(product_count=Count('id'))
#     return total_products_per_category

# def total_stock_per_product_category():
#     total_products_per_category= Product.objects.values('cat_id__name').annotate(quantity=sSum('quantity'))
#     return total_products_per_category