from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from IOT.models import UserProfile, Sensor, User, SensorValueStore
from IOT.serializers import UserProfileCreateSerializer, UserProfileSerializer, SensorSerializer
from IOT.permissions import FullDjangoModelPermissions

from datetime import datetime, timedelta


class UserProfileCreate(ListCreateAPIView):

    permission_classes = [IsAuthenticated, FullDjangoModelPermissions]

    def get_queryset(self):
        return UserProfile.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        return UserProfileCreateSerializer

    def get(self, request):
        queryset = get_object_or_404(UserProfile, user_id=request.user.id)
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
        queryset = get_object_or_404(UserProfile, user_id=request.user.id)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)
    
    def put(self, request):
        queryset = get_object_or_404(UserProfile, user_id=request.user.id)
        serializer = UserProfileSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request):
        queryset = get_object_or_404(UserProfile, user_id=request.user.id)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
class SensorList(ListAPIView):

   # permission_classes = [IsAuthenticated, FullDjangoModelPermissions]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    ordering_fields = ['id', 'name', 'value', 'user']
    search_fields = ['name']

    def get_queryset(self):
        # if self.request.user.is_staff:
        #     query_set = Sensor.objects.select_related('user').all().order_by('id')
        #     return query_set
        query_set = Sensor.objects.select_related('user').filter(user_id=7).order_by('id')
        return query_set
    
    def get_serializer_class(self):
        return SensorSerializer



class SensorDetail(RetrieveAPIView):

    #permission_classes = [IsAuthenticated, FullDjangoModelPermissions]
    
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Sensor.objects.select_related('user').filter(user__id=7).filter(pk=pk)
        return queryset
    
    def get_serializer_class(self):
        return SensorSerializer
    
    def get(self, request, pk):
        queryset = get_object_or_404(Sensor.objects.select_related('user').filter(user__id=7), pk=pk)
        serializer = SensorSerializer(queryset)
        return Response(serializer.data)
    


class ParticularSensorUpdate(RetrieveUpdateAPIView):

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Sensor.objects.select_related('user').filter(pk=pk)
        return queryset
    
    def get_serializer_class(self):
        return SensorSerializer
    
    def get(self, request, pk):
        queryset = get_object_or_404(Sensor.objects.select_related("user"), id=pk)
        if queryset.user_id == request.user.id:
            serializer = SensorSerializer(queryset)
            return Response(serializer.data)
        else:
            return Response({"detail": "You can only view your sensor"}, status=status.HTTP_403_FORBIDDEN)
            
    
    def put(self, request, pk):
        queryset = get_object_or_404(Sensor, id=pk)
        user = User.objects.get(id=queryset.user_id)
        if str(queryset.user.username) == "aachal":
            if request.data["user"] == user.id:
                serializer = SensorSerializer(queryset, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                new_instance = SensorValueStore()
                new_instance.value = float(request.data["value"])
                new_instance.sensor_id = int(pk)
                new_instance.save()

                return Response({"detail": "update successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "cannot change user id"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "another user update. Update the sensors of Aachal only.."}, status=status.HTTP_403_FORBIDDEN)



class LastWeekAverage(APIView):

    #permission_classes = [IsAuthenticated]
    
    def get(self, request, index):
        
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        if index == "temperature":
            queryset = SensorValueStore.objects.filter(sensor_id=12).filter(date__gt=seven_days_ago).aggregate(avg_value=Avg('value'))
            average =  queryset['avg_value']
            return Response({"average": average}, status=status.HTTP_200_OK)
        
        elif index == "moisture":
            queryset = SensorValueStore.objects.filter(sensor_id=13).filter(date__gt=seven_days_ago).aggregate(avg_value=Avg('value'))
            average =  queryset['avg_value']
            return Response({"average": average}, status=status.HTTP_200_OK)
        
        elif index == "humidity":
            queryset = SensorValueStore.objects.filter(sensor_id=14).filter(date__gt=seven_days_ago).aggregate(avg_value=Avg('value'))
            average =  queryset['avg_value']
            return Response({"average": average}, status=status.HTTP_200_OK)
        
        else:
            return Response({"detail": "error index"}, status=status.HTTP_404_NOT_FOUND)