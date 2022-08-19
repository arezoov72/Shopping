

from ast import Delete
from itertools import product
from multiprocessing import context
from operator import imod
from urllib import response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from  rest_framework.response import Response
from store.Pagination import DefaultPaginations
from store.filters import ProductFilter
from .models import Cart, Collection, OrderItem, Product,Review
from .serializers import CartSerializer, ProductSerializer,CollectionSerializer,ReviewSErializer
from django.db.models.aggregates import Count
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import GenericViewSet
# Create your views here.


class ProductList(ListCreateAPIView):
  
    queryset=Product.objects.select_related('collection').all()
    serializer_class=ProductSerializer
    def get_serializer_context(self):
        return {'request':self.request}

        

#in order to use def
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method=='GET':
#         queryset=Product.objects.select_related('collection').all()
#         #use many=true to know we should itrate the queryset and convert all to dict
#         #adding request is for collection field in serializers
#         serializer=ProductSerializer(queryset,many=True, context={'request':request})
#         return Response(serializer.data)
#     elif request.method=='POST':
#         #diserialize
#         serializer=ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()
#         return Response(serializer.data,status =status.HTTP_201_CREATED)
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    #beacus it has conditions we use delete
    def delete(self,request,pk):
        product=get_object_or_404(Product,pk=pk)
        if product.orderitems.count()>0:
            return Response({'error':'product can not be deletd'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete
        return Response(status==status.HTTP_204_NO_CONTENT)

# @api_view(['GET','PUT','DELETE'])
# def product_detail(request,id):
#     # try:
#     #     product=Product.objects.get(pk=id)
#     #     serializer=ProductSerializer(product)
#     #     return Response(serializer.data)
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)


#     product=get_object_or_404(Product,pk=id)
#     if request.method=='GET':
#         serializer=ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method=='PUT':
#         serializer=ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return response(serializer.data)
#     elif request.method=='DELETE':
#         if product.orderitems.count()>0:
#             return Response({'error':'product can not be deletd'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete
#         return Response(status==status.HTTP_204_NO_CONTENT)




class CollectionList(ListCreateAPIView):
    queryset=Collection.objects.annotate(
        products_count=Count('product')).all()
    serializer_class=CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset=Collection.objects.annotate(
        products_count=Count('product')
    )
    serializer_class=CollectionSerializer
    def delete(self,request,pk):
        collection=get_object_or_404(Product,pk=pk)
        if collection.products.count()>0:
            return Response({'error':'product can not be deletd'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete
        return Response(status==status.HTTP_204_NO_CONTENT)

# @api_view(['GET','PUT','DELETE'])    
# def collection_detail(request,pk):
#     collection=get_object_or_404(Product,pk=id)
#     Collection.objects.annotate(
#         products_count=Count('product'), pk=pk
#     )
#     if request.method=='GET':
#         serializer=CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method=='PUT':
#         serializer=CollectionSerializer(collection,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return response(serializer.data)
#     elif request.method=='DELETE':
#         if collection.products.count()>0:
#             return Response({'error':'product can not be deletd'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete
#         return Response(status==status.HTTP_204_NO_CONTENT)
 
from rest_framework.viewsets import ModelViewSet
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.select_related('collection').all()
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['title','description']
    ordering_fields=['unit_price','last_update']
    pagination_class=DefaultPaginations
    serializer_class=ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    #we want to see delete only in detail list
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
            return Response({'error':'product can not be deletd'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(
    products_count=Count('product')).all()
    serializer_class=CollectionSerializer
    def delete(self,request,pk):
        collection=get_object_or_404(Product,pk=pk)
        if collection.products.count()>0:
            return Response({'error':'product can not be deletd'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete
        return Response(status==status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
   
    serializer_class=ReviewSErializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


#becuse we need custom view we have Get,post and delete so we cant use viewset
class CartViewset(CreateModelMixin,GenericViewSet):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer




