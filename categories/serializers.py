from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Category

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for category objects
    """
    class Meta:
        model = Category
        fields = ['user', 'category']

class LinkedCategorySerializer(CategorySerializer):
    """
    Serializer for the category objects when nested in users
    """
    def get_fields(self, *args, **kwargs):
        fields = super(LinkedCategorySerializer, self).get_fields(*args, **kwargs)
        fields['user'].read_only = True
        return fields