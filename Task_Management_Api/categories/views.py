from django.shortcuts import render
from rest_framework import generics, response, status, pagination
from django.db import models

from .serializers import CategorySerializer
from .models import Category

# Create your views here.
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user =self.request.user
        return Category.objects.filter(models.Q(author=user) | models.Q(author__isnull=True))
    
    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(author=self.request.user)
        else:
            serializer.save(author=None)
        #return super().perform_create(serializer)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        user =self.request.user
        return Category.objects.filter(models.Q(author=user) | models.Q(author__isnull=True))

    def perform_update(self, serializer: CategorySerializer):
        category = self.get_object()

        ## Condition to allow admins to modify default category
        if not category.author and self.request.user.is_staff:
            serializer.save()

        ## return an error if the user is not the author of the category
        elif category.author and category.author != self.request.user:
            raise response.Response(status=status.HTTP_401_UNAUTHORIZED, data="user unauthorised to modify this category")
        
        else:
            serializer.save()

       
    
    def perform_destroy(self, instance: Category):

        ## Condition to allow admins to delete default category
        if not instance.author and self.request.user.is_staff:
            instance.delete()

        ## allow user to delete the category he/she created
        elif instance.author and instance.author != self.request.user:
            return response.Response(status=status.HTTP_401_UNAUTHORIZED, data="user unauthorised to delete this category")
        
        else:
            instance.delete()
        