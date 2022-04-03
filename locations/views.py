from rest_framework import viewsets
from .serializers import LocationSerializer
from .serializers import TimePeriodSerializer, BaseLocationSerializer
from .serializers import TempLocationSerializer
from .models import Location, TimePeriod
from .models import BaseLocation, TempLocation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """
    serializer_class = LocationSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Overwrite queryset for filtering
        """
        # first get all objects
        queryset = Location.objects.all()

        """ Values filtering """
        # Part string search filtering in city OR country
        search_string = self.request.GET.get('s')
        if search_string is not None:
            queryset = queryset.filter(city__icontains=search_string) | queryset.filter(country__icontains=search_string)
        # base location city filtering (nested object)
        city = self.request.GET.get('city')
        if city is not None:
            queryset = queryset.filter(city=city)
        # base location country filtering (nested object)
        country = self.request.GET.get('country')
        if country is not None:
            queryset = queryset.filter(country=country)
        # base location latitude filtering (nested object)
        latitude = self.request.GET.get('latitude')
        if latitude is not None:
            queryset = queryset.filter(latitude=latitude)
        # base location longitude filtering (nested object)
        longitude = self.request.GET.get('longitude')
        if longitude is not None:
            queryset = queryset.filter(longitude=longitude)

        return queryset

    """
    Swagger manual information added for documentation building
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('s',
            openapi.IN_QUERY,
            description='Allows part-match filtering on first_name OR last_name (both results combined, ex: ?s=Cabar).',
            type=openapi.TYPE_STRING),
            openapi.Parameter('city',
            openapi.IN_QUERY,
            description='Allows exact match filtering on city (Ex: ?city=Cabarete).',
            type=openapi.TYPE_STRING),
            openapi.Parameter('country',
            openapi.IN_QUERY,
            description='Allows exact match filtering on country (Ex: ?country=Dominican Republic).',
            type=openapi.TYPE_STRING),
            openapi.Parameter('longitude',
            openapi.IN_QUERY,
            description='Allows exact match filtering on longitude (Ex: ?longitude=19.0).',
            type=openapi.TYPE_STRING),
            openapi.Parameter('latitude',
            openapi.IN_QUERY,
            description='Allows exact match filtering on latitude (Ex: ?latitude=-70.0).',
            type=openapi.TYPE_STRING),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super(LocationViewSet, self).list(request, *args, **kwargs)