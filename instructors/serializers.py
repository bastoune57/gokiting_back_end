from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User, Language, Category
from locations.models import BaseLocation, TempLocation
from locations.serializers import BaseLocationSerializer, TempLocationSerializer


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for drf group class 
    """
    class Meta:
        model = Group
        fields = ['url', 'name']

class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for language objects
    """
    class Meta:
        model = Language
        fields = ['url', 'user', 'language']

class NestedLanguageSerializer(LanguageSerializer):
    """
    Serializer for the language objects when nested in users
    """
    def get_fields(self, *args, **kwargs):
        fields = super(NestedLanguageSerializer, self).get_fields(*args, **kwargs)
        fields['user'].read_only = True
        return fields

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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for users objects
    """
    # declare nested objects
    #many=True
    categories = LinkedCategorySerializer(required=False, many=True)
    languages = NestedLanguageSerializer(required=False, many=True)
    baselocations = BaseLocationSerializer(required=False, many=True)
    templocations = TempLocationSerializer(required=False, many=True)
    class Meta:
        model = User
        fields = ['id', 'url', 'email', 'first_name',
                  'last_name', 'is_instructor', 'avatar_url',
                  'rating', 'phone', 'title', 'description',
                  'languages' ,'categories', 'baselocations',
                  'templocations']

    def create(self, validated_data):
        """
        Overwrite create for nested objects
        """
        # declare nested variables
        categories_data = None
        languages_data = None
        baselocations_data = None
        templocations_data = None

        # extract nested objects from input dict if they exist
        if 'categories' in validated_data.keys():
            categories_data = validated_data.pop('categories')
        if 'languages' in validated_data.keys():
            languages_data = validated_data.pop('languages')
        if 'baselocations' in validated_data.keys():
            baselocations_data = validated_data.pop('baselocations')
        if 'templocations' in validated_data.keys():
            templocations_data = validated_data.pop('templocations')

        # create user object from resulting input dict 
        user = User.objects.create(**validated_data)

        # if there were categories then add it/them
        if categories_data is not None:
            for item in categories_data:
                Category.objects.create(user=user, **item)
        # if there were languages then add it/them
        if languages_data is not None:
            for item in languages_data:
                Language.objects.create(user=user, **item)
        # if there were base locations then add it/them
        if baselocations_data is not None:
            for item in baselocations_data:
                BaseLocation.objects.create(user=user, **item)
        # if there were temp locations then add it/them
        if templocations_data is not None:
            for item in templocations_data:
                TempLocation.objects.create(user=user, **item)
        
        # return created user
        return user

# # Serializer for users objects to use for PUT and PATCH request
# class ModifyUserSerializer(UserSerializer):
#     def get_fields(self, *args, **kwargs):
#         fields = super(ModifyUserSerializer, self).get_fields(*args, **kwargs)
#         fields['email'].read_only = True
#         return fields