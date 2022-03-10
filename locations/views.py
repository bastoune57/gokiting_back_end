from rest_framework import viewsets
from .serializers import LocationSerializer
from .serializers import TimePeriodSerializer, BaseLocationSerializer
from .serializers import TempLocationSerializer
from .models import Location, TimePeriod
from .models import BaseLocation, TempLocation

class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    #permission_classes = [permissions.IsAuthenticated]

class BaseLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows base locations to be viewed or edited.
    """
    queryset = BaseLocation.objects.all()
    serializer_class = BaseLocationSerializer
    #permission_classes = [permissions.IsAuthenticated]

class TempLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows temporary locations to be viewed or edited.
    """
    queryset = TempLocation.objects.all()
    serializer_class = TempLocationSerializer
    #permission_classes = [permissions.IsAuthenticated]

class TimePeriodViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows time periods to be viewed or edited.
    """
    queryset = TimePeriod.objects.all()
    serializer_class = TimePeriodSerializer
    #permission_classes = [permissions.IsAuthenticated]

