from django.shortcuts import render
from .models import Language
from .serializers import LanguageSerializer

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Count

# Create your views here.

class LanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows languages to be viewed or edited.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    #permission_classes = [permissions.IsAuthenticated]

class StatsLanguageView(generics.ListAPIView):
    """
    API endpoint that allows languages statistics to be viewed.
    """
    serializer_class = LanguageSerializer
    def summarize(self, request, *args, **kwargs):
        """This can be moved to a Mixin class."""
        # make sure the filters of the parent class get applied
        queryset = Language.objects.values('language').annotate(language_count=Count('pk')).order_by('language')
        return Response(queryset)

    def get(self, request, *args, **kwargs):
        return self.summarize(request, *args, **kwargs)