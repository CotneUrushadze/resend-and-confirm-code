from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated

from categories.models import Category, CategoryImage
from categories.serializers import CategorySerializer, CategoryDetailSerializer, CategoryImageSerializer
from rest_framework.viewsets import GenericViewSet




class CategoryListView(GenericViewSet, ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

 



class CategoryDetailView(GenericViewSet, ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    





class CategoryImageViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_pk']
        return self.queryset.filter(category=category_id)
    
