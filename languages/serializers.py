from .models import Language
from rest_framework import serializers

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