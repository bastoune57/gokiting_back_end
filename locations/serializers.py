
from rest_framework import serializers
from .models import Location, TimePeriod, BaseLocation
from .models import TempLocation
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


''' DIRECT OBJECT SERIALIZERS '''


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Location objects
    """
    class Meta:
        model = Location
        fields = ['id', 'url', 'city', 'country', 'longitude', 'latitude']

class BaseLocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for base Location objects
    """
    class Meta:
        model = BaseLocation
        fields = ['id', 'url', 'user', 'location']

class TimePeriodSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for time period objects
    """
    class Meta:
        model = TimePeriod
        fields = ['id', 'url', 'start_date', 'end_date']
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must occur after start date")
        return data

class TempLocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for temporary Location objects
    """
    class Meta:
        model = TempLocation
        fields = ['id', 'url', 'user', 'location', 'timeperiod']


''' NESTED OBJECT SERIALIZERS '''

class NestedTimePeriodSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for nested Location objects. (get_or_create)
    """
    class Meta:
        model = TimePeriod
        fields = ['url', 'start_date', 'end_date']
        validators = [] # remove validators for nested objects as we do not know if they already exists

class NestedLocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for nested Location objects. (get_or_create)
    """
    class Meta:
        model = Location
        fields = ['url', 'city', 'country', 'longitude', 'latitude']
        validators = [] # remove validators for nested objects as we do not know if they already exists


''' NESTED OBJECT CREATION SERIALIZERS '''


class CreateNestedBaseLocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for creating nested base Location objects
    """
    location = NestedLocationSerializer(required=False)
    class Meta:
        model = BaseLocation
        fields = ['location']

class CreateNestedTempLocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for creating nested temp Location objects
    """
    location = NestedLocationSerializer(required=True)
    timeperiod = NestedTimePeriodSerializer(required=True)
    class Meta:
        model = TempLocation
        fields = ['location', 'timeperiod']

def add_or_create_base_location (user, baselocations_data):
    """
    Check if object already exists in DB or create it
    then connect it to the base location
    """
    for item in baselocations_data:
        # for each item of the list
        if 'location' in item.keys():
            # get the location data
            location_data = item.pop('location')
            # retrieve or create it in DB
            location, created = Location.objects.get_or_create(**location_data)
            # Add index in indexing table (get or create to avoid duplicates)
            BaseLocation.objects.get_or_create(user=user, location=location)