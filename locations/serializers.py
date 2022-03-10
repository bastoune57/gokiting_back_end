
from rest_framework import serializers

from .models import Location, TimePeriod, BaseLocation
from .models import TempLocation

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Location objects
    """
    class Meta:
        model = Location
        fields = ['url', 'city', 'country', 'ZIP', 'longitude', 'latitude']


class BaseLocationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for base Location objects
    """
    location = LocationSerializer(required=False)
    class Meta:
        model = BaseLocation
        fields = ['url', 'user', 'location']
        
    # def to_representation(self, value):
    #     duration = time.strftime('%M:%S', time.gmtime(value.duration))
    #     return 'Track %d: %s (%s)' % (value.order, value.name, duration)

class TimePeriodSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for time period objects
    """
    class Meta:
        model = TimePeriod
        fields = ['url', 'start_date', 'end_date']
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
        fields = ['url', 'user', 'location', 'timeperiod']