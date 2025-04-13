from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from products.models import Product, Review, FavoriteProduct, Cart, ProductTag, ProductImage, CartItem
from products.serializers import ProductSerializer, ReviewSerializer, FavoriteProductSerializer, CartSerializer, CartItemSerializer, ProductTagSerializer, ProductImageSerializer
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import SearchFilter 
from products.pagination import ProductPagination
from products.filters import ProductFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
from products.permissions import IsObjectOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser


class ProductViewSet(ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_class = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    pagination_class = ProductPagination 
    throttle_classes = [UserRateThrottle]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_products(self, request):
        products = Product.objects.filter(user=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    
        
class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_class = [IsAuthenticated, IsObjectOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
    

    
    
class FavoriteProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_class = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'likes'
    # http_method_names = ['get', 'post', 'delete']
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    

     

class CartViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_class = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset




class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.cart.user != self.request.user:
            raise PermissionDenied("you do not have permission to delete this")
        instance.delete()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.cart.user != self.request.user:
            raise PermissionDenied("you do not have permission to update this")
        serializer.save()



class ProductTagViewSet(GenericViewSet, ListModelMixin):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer
    permission_class = [IsAuthenticated]




class ProductImageViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_class = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    
    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs['product_pk'])
    
    # def create(self, *args, **kwargs):
    #     try:
    #         super().create()
        
    
