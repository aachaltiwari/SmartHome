from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from IOT.models import UserProfile, Sensor
from IOT.serializers import UserProfileCreateSerializer, UserProfileSerializer, SensorSerializer
from IOT.permissions import FullDjangoModelPermissions



class UserProfileCreate(ListCreateAPIView):

    permission_classes = [IsAuthenticated, FullDjangoModelPermissions]

    def get_queryset(self):
        return UserProfile.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        return UserProfileCreateSerializer

    def get(self, request):
        queryset = get_object_or_404(UserProfile.objects.filter(user_id=request.user.id))
        serializer = UserProfileCreateSerializer(queryset)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.id) != str(request.data['user']):
            return Response({"detail":"user cannot be changed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



class UserProfileDetail(RetrieveUpdateDestroyAPIView):

    http_method_names = ['get', 'put', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated, FullDjangoModelPermissions]

    def get_queryset(self):
        return UserProfile.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        return UserProfileSerializer

    def get(self, request):
        queryset = get_object_or_404(UserProfile.objects.filter(user_id=request.user.id))
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)
    
    def put(self, request):
        queryset = get_object_or_404(UserProfile.objects.filter(user_id=request.user.id))
        serializer = UserProfileSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request):
        queryset = get_object_or_404(UserProfile.objects.filter(user_id=request.user.id))
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
class SensorList(ListAPIView):

    permission_classes = [IsAuthenticated, FullDjangoModelPermissions]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    ordering_fields = ['id', 'name', 'value', 'user']
    search_fields = ['name']

    def get_queryset(self):
        if self.request.user.is_staff:
            query_set = Sensor.objects.select_related('user').all().order_by('id')
            return query_set
        query_set = Sensor.objects.select_related('user').filter(user_id=self.request.user.id).order_by('id')
        return query_set
    
    def get_serializer_class(self):
        return SensorSerializer



class SensorDetail(RetrieveAPIView):

    permission_classes = [IsAuthenticated, FullDjangoModelPermissions]

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Sensor.objects.select_related('user').filter(user__id=self.request.user.id).filter(pk=pk)
        return queryset
    
    def get_serializer_class(self):
        return SensorSerializer
    
    def get(self, request, pk):
        queryset = get_object_or_404(Sensor.objects.select_related('user').filter(user__id=self.request.user.id), pk=pk)
        serializer = SensorSerializer(queryset)
        return Response(serializer.data)