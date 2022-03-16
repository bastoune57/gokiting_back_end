from rest_framework import viewsets
from django.shortcuts import render
from django.db.models import Count
from rest_framework import generics
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [permissions.IsAuthenticated]

class StatsCategoryView(generics.ListAPIView):
    """
    API endpoint that allows categories statistics to be viewed.
    """
    serializer_class = CategorySerializer
    def summarize(self, request, *args, **kwargs):
        """This can be moved to a Mixin class."""
        # make sure the filters of the parent class get applied
        queryset = Category.objects.values('category').annotate(category_count=Count('pk')).order_by('category')
        return Response(queryset)

    def get(self, request, *args, **kwargs):
        return self.summarize(request, *args, **kwargs)
