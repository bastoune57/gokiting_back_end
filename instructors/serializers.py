from django.contrib.auth.models import Group
from rest_framework import serializers

from locations.models import BaseLocation, TempLocation

from .models import User
from languages.models import Language
from languages.serializers import NestedLanguageSerializer
from categories.models import Category
from categories.serializers import LinkedCategorySerializer
from locations.serializers import CreateNestedBaseLocationSerializer
from locations.serializers import TempLocationSerializer, add_or_create_base_location

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for drf group class 
    """
    class Meta:
        model = Group
        fields = ['url', 'name']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for users objects
    """
    # declare nested objects
    #many=True
    categories = LinkedCategorySerializer(required=False, many=True)
    languages = NestedLanguageSerializer(required=False, many=True)
    baselocations = CreateNestedBaseLocationSerializer(required=False, many=True)
    templocations = TempLocationSerializer(required=False, many=True)
    class Meta:
        model = User
        fields = ['id', 'url', 'email', 'first_name',
                  'last_name', 'is_instructor', 'avatar_url',
                  'rating', 'phone', 'title', 'description',
                  'languages' ,'categories', 'baselocations',
                  'templocations']

    
    def remove_nested_objects(self, user):
        """
        Function to remove nested objects
        """
        # categories
        Category.objects.filter(user=user).delete()
        # languages
        Language.objects.filter(user=user).delete()
        # base locations
        BaseLocation.objects.filter(user=user).delete()
        # temp locations
        TempLocation.objects.filter(user=user).delete()

    def update_nested_objects(self, user, validated_data):
        """
        Function to update/create nested objects
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
            locations_list = add_or_create_base_location(user=user, baselocations_data=baselocations_data)
        # if there were temp locations then add it/them
        if templocations_data is not None:
            for item in templocations_data:
                TempLocation.objects.create(user=user, **item)
        
        # return created user
        return user


    def create(self, validated_data):
        """
        Overwrite create for nested objects
        """

        #save copy of input dict
        validated_data_cp = validated_data.copy()

        # extract nested objects from input dict if they exist
        if 'categories' in validated_data.keys():
            categories_data = validated_data.pop('categories')
        if 'languages' in validated_data.keys():
            languages_data = validated_data.pop('languages')
        if 'baselocations' in validated_data.keys():
            baselocations_data = validated_data.pop('baselocations')
        if 'templocations' in validated_data.keys():
            templocations_data = validated_data.pop('templocations')

        # create user object from validated input data
        user = User.objects.create(**validated_data)

        # Update Nested objects
        self.update_nested_objects(user, validated_data_cp)

        # return created user
        return user

    def update(self, instance, validated_data):
        """
        Overwrite update for nested objects
        """
        # update instance fields
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_instructor = validated_data.get('is_instructor', instance.is_instructor)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        # remove all nested objects
        self.remove_nested_objects(instance) 
        # Update Nested objects
        self.update_nested_objects(instance, validated_data)
        return instance

# # Serializer for users objects to use for PUT and PATCH request
# class ModifyUserSerializer(UserSerializer):
#     def get_fields(self, *args, **kwargs):
#         fields = super(ModifyUserSerializer, self).get_fields(*args, **kwargs)
#         fields['email'].read_only = True
#         return fields
