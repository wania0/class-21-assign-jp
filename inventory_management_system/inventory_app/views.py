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
from .serializers import ProductSerializer, ProductUpdateSerializer


from django.db.models import Count, Sum, Avg

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


@api_view(['GET'])
def get_category_metrics(request: Request):
    data = []
    category_product_count = category_model.objects.annotate(
    total_products=Count('product__id')).values('id', 'name', 'total_products')
    data.append({'category_product_count':category_product_count})
    
    category_stock_quantity = category_model.objects.annotate(
    total_stock=Sum('product__quantity')).values('id', 'name', 'total_stock')
    data.append({'category_stock_quantity' : category_stock_quantity})
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

@api_view(['GET'])
def get_supplier_metrics(request: Request):
    data = []
    products_per_supplier = (product_model.objects.values('supplier__id', 'supplier__name').annotate(total_products=Count('id')) )
    data.append({'products_per_supplier':products_per_supplier})
    
    max_products_supplied = products_per_supplier.order_by('-total_products').first()
    data.append({'max_products_supplied' : max_products_supplied})
    
    min_products_supplied = products_per_supplier.order_by('total_products').first()
    data.append({'min_products_supplied' : min_products_supplied})
    return Response(data, status=status.HTTP_200_OK)
    


# product
@api_view(['GET', 'POST'])
def get_products_or_create_product(request: Request):
    data = []
    if request.method == 'GET':
        params = request.query_params
        
        product_objects = product_model.objects.all()
        if params.get("name") is not None:
            product_objects = product_objects.filter(name=params.get("name"))

        if params.get("id") is not None:
           product_objects =product_objects.filter(id=params.get("id"))
           
        if params.get("category_id") is not None:
           product_objects =product_objects.filter(category_id=params.get("category_id"))
           
        if params.get("supplier_id") is not None:
           product_objects =product_objects.filter(supplier_id=params.get("supplier_id"))

        products = product_objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
    if request.method == 'POST':
        serializer = ProductSerializer(data= request.data)
        if serializer.is_valid():
            cat_id = serializer.validated_data.pop("category_id")
            category = category_model.objects.get(pk=cat_id)
            if category is None:
                return Response("category not found")
            supplier_ids = serializer.validated_data.pop("supplier_id", [])
            db_suppliers = supplier_model.objects.filter(id__in=supplier_ids).all()
            if len(db_suppliers) != len(supplier_ids):
                return Response("One or more supplier IDs are invalid.", status=status.HTTP_400_BAD_REQUEST)
            product =  product_model.objects.create(category=category, **serializer.validated_data)
            product.supplier.set(supplier_ids)
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
        serializer = ProductUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            
            category_id = serializer.validated_data['category_id']
            category = category_model.objects.get(pk=category_id)
            product.category = category
            supplier_ids = serializer.validated_data['supplier_id']
            supplier = supplier_model.objects.filter(id__in=supplier_ids).all()
            product.save()
            product.supplier.set(supplier)

        else:
            return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        data = "product updated successfully"
        return Response(data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        product.delete()
        data = "deleted"

    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_product_metrics(request: Request):
    data = []
    
    #product metrics
    total_products = product_model.objects.count()
    data.append({'total_products': total_products})
    
    products_per_category = (
        product_model.objects.values('category_id')
        .annotate(total_products=Count('id'))
    )
    data.append({'products_per_category':products_per_category})
    
    products_per_supplier = (
        product_model.objects.values('supplier__id')
        .annotate(total_products=Count('id'))
    )
    data.append({'products_per_supplier':products_per_supplier})
    
    stock_quantity_per_category = (
        product_model.objects.values('category_id')
        .annotate(total_stock=Sum('quantity'))
    )
    data.append({'stock_quantity_per_category' : stock_quantity_per_category})

    avg_price_per_category = (
        product_model.objects.values('category_id')
        .annotate(avg_price=Avg('price'))
    )
    data.append({'avg_price_per_category': avg_price_per_category})
    return Response(data, status=status.HTTP_200_OK)

