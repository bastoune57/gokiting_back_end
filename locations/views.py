from asyncio.log import logger
from django.http import HttpResponseBadRequest
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from .serializers import LocationSerializer
from .serializers import TimePeriodSerializer, BaseLocationSerializer
from .serializers import TempLocationSerializer
from .models import Location, TimePeriod
from .models import BaseLocation, TempLocation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from . import helpers
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

import logging

from locations import serializers

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['city', 'country', 'latitude', 'longitude']
    # search_fields = ['city', 'country']
    #permission_classes = [permissions.IsAuthenticated]

    # def validate(self):
    #     """
    #     Overwrite queryset to validate filtering options
    #     """
    #     logger.error('I AM HERRE !!!!!!')
    #     if 'latitude' in self.request.GET:
    #         latitude = self.request.GET.get('latitude')
    #         if float(latitude) > 90 or float(latitude) > -90:
    #             raise HttpResponseBadRequest("Wrong latitude filter value {}. Must be between -+90°.".format(latitude) )
    #     if 'longitude' in self.request.GET:
    #         longitude = self.request.GET.get('longitude')
    #         if float(longitude) > 180 or float(longitude) > -180:
    #             raise HttpResponseBadRequest("Wrong longitude filter value: {}. Must be between -+180°.".format(longitude) )

    def get_queryset(self):
        """
        Overwrite queryset for filtering
        """
        # first validate filtering options
        #self.validate()

        # second get all objects
        queryset = Location.objects.all()
        
        """ Values filtering """
        # Part string search filtering in city OR country
        if 'search' in self.request.GET:
            search_string = self.request.GET.get('search')
            queryset = queryset.filter(city__icontains=search_string) | queryset.filter(country__icontains=search_string)
        # location city filtering (nested object)
        if 'city' in self.request.GET:
            city = self.request.GET.get('city')
            queryset = queryset.filter(city=city)
        # location country filtering (nested object)
        if 'country' in self.request.GET:
            country = self.request.GET.get('country')
            queryset = queryset.filter(country=country)
        # location latitude filtering (nested object)
        latitude = self.request.GET.get('latitude')
        if latitude is not None:
            queryset = queryset.filter(latitude=latitude)
        # location longitude filtering (nested object)
        longitude = self.request.GET.get('longitude')
        if longitude is not None:
            queryset = queryset.filter(longitude=longitude)
        # location get 5 nearest if no exact result for latitude & longitude search
        if (latitude is not None) and (longitude is not None) and (queryset.count() == 0):
            # first get all objects
            queryset = Location.objects.all()
            target = {'latitude': latitude, 'longitude':longitude}
            # XXX list of queryset loads all db in memory... To be optimized at least
            res = helpers.sort_to_closest(queryset, target, 6)
            #logger.error(res)
            queryset = res

        return queryset

    """
    Swagger manual information added for documentation building
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search',
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
            description='Allows exact match filtering on longitude (Ex: ?longitude=19.0). NOTE: When longitude and latitude are specified but no exact result is found then the 6 nearest locations are displayed.',
            type=openapi.TYPE_STRING),
            openapi.Parameter('latitude',
            openapi.IN_QUERY,
            description='Allows exact match filtering on latitude (Ex: ?latitude=-70.0). NOTE: When longitude and latitude are specified but no exact result is found then the 6 nearest locations are displayed.',
            type=openapi.TYPE_STRING)
        ],
    )
    def list(self, request, *args, **kwargs):
        return super(LocationViewSet, self).list(request, *args, **kwargs)