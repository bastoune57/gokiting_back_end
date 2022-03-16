from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializer#, ModifyUserSerializer
from .serializers import LanguageSerializer, CategorySerializer
from .serializers import GroupSerializer
from django.contrib.auth.models import Group
from .models import User, Language, Category

from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

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

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = [permissions.IsAuthenticated]

class StatsCategoryView(generics.ListAPIView):
    """
    API endpoint that allows categories statistics to be viewed.
    """
    serializer_class = CategorySerializer
    def summarize(self, request, *args, **kwargs):
        """This can be moved to a Mixin class."""
        # make sure the filters of the parent class get applied
        queryset = Category.objects.values('category').annotate(category_count=Count('pk')).order_by('category')
        return Response(queryset)

    def get(self, request, *args, **kwargs):
        return self.summarize(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer(self, *args, **kwargs):
        """ 
        Overwrite get_serializer to allow the creation of several users
        if an array is passed, set serializer to many 
        """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(UserViewSet, self).get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        """
        # Overwrite get_serializer_class to specify which 
        # serializer to use depending on the kind of request:
        # create, list, retrieve, update, partial_update, and destroy
        # POST,   GET,  GET,      PUT,    PATCH               DELETE
        """
        # if self.action in ['update', 'partial_update']: 
        #     return ModifyUserSerializer
        # if self.action == 'retrieve':
        #     return UserDetailsSerializer
        return UserSerializer

    def get_queryset(self):
        """
        Overwrite queryset for filtering
        """
        # first get all objects
        queryset = User.objects.all()

        """ Values filtering"""
        # id filtering
        uid = self.request.GET.get('id')
        if uid is not None:
            queryset = queryset.filter(id=uid)
        # rating filtering
        rating = self.request.GET.get('rating')
        if rating is not None:
            queryset = queryset.filter(rating=rating)
        # last_name filtering
        last_name = self.request.GET.get('last_name')
        if last_name is not None:
            queryset = queryset.filter(last_name=last_name)
        # first_name filtering
        first_name = self.request.GET.get('first_name')
        if first_name is not None:
            queryset = queryset.filter(first_name=first_name)
        # language filtering (nested object)
        language = self.request.GET.get('language')
        if language is not None:
            id_list = Language.objects.filter(language=language).values_list('user_id', flat=True)
            queryset = queryset.filter(pk__in=id_list)
        
        """ SORTING filtering"""
        asc = self.request.GET.get('asc')
        desc = self.request.GET.get('desc')
        # asc filtering
        if asc is not None:
            queryset = queryset.order_by(''+asc)
        # DESC filtering
        elif desc is not None:
            queryset = queryset.order_by('-'+desc)
        # default ordering by date_joined
        else:
            queryset.order_by('-date_joined')

        return queryset

    """
    Swagger manual information added for documentation building
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id',
            openapi.IN_QUERY,
            description='Allows exact match filtering on id',
            type=openapi.TYPE_INTEGER),
            openapi.Parameter('rating',
            openapi.IN_QUERY,
            description='Allows exact match filtering on rating',
            type=openapi.TYPE_INTEGER),
            openapi.Parameter('last_name',
            openapi.IN_QUERY,
            description='Allows exact match filtering on last_name',
            type=openapi.TYPE_STRING),
            openapi.Parameter('first_name',
            openapi.IN_QUERY,
            description='Allows exact match filtering on first_name',
            type=openapi.TYPE_STRING),
            openapi.Parameter('language',
            openapi.IN_QUERY,
            description='Allows exact match filtering on language (Ex: ?language=en).',
            type=openapi.TYPE_STRING),
            openapi.Parameter('asc',
            openapi.IN_QUERY,
            description='Allows ascending sorting of the results based on field names (Ex: ?asc=last_name). It is dominant compared to desc filtering.',
            type=openapi.TYPE_STRING),
            openapi.Parameter('desc',
            openapi.IN_QUERY,
            description='Allows descending sorting of the results based on field names (Ex: ?desc=last_name). If asc is specified, desc filtering is canceled',
            type=openapi.TYPE_STRING),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)