from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import CollectionSerializer, ProductSerializer
from .models import Collection, Product
from django.db.models.aggregates import Count

# class ProductList(APIView):
#     def get(self,request):
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(query_set,many= True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    def get_serializer_context(self):
        return {'request':self.request}
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count = Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request':self.request}

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # def get(self,request,pk):
    #     product = get_object_or_404(Product,pk=pk)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    # def put(self,request,pk):
    #     product = get_object_or_404(Product,pk=pk)
    #     serializer = ProductSerializer(product,data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    def delete(self,request,pk):
        product = get_object_or_404(Product,pk=pk)
        if product.orderitem_set.count()>0:
            return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response (status=status.HTTP_204_NO_CONTENT) 

# class CollectionList(APIView):
#     def get(self,request):
#         query_set = Collection.objects.annotate(products_count = Count('products')).all()
#         serializer = CollectionSerializer(query_set,many= True)
#         return Response(serializer.data)
#     def post(self,request):
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
    
class CollectionDetail(APIView):
    def get(self,request,pk):
        collection = get_object_or_404(
        Collection.objects.annotate(products_count = Count('products'))
        ,pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    def post(self,request,pk):
        collection = get_object_or_404(
        Collection.objects.annotate(products_count = Count('products'))
        ,pk=pk)
        serializer = CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self,request,pk):
        collection = get_object_or_404(
        Collection.objects.annotate(products_count = Count('products'))
        ,pk=pk)
        if collection.products.count()>0:
            return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response (status=status.HTTP_204_NO_CONTENT) 
