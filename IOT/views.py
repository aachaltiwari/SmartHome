from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F

#from rest_framework.decorators import api_view -> for function api view
#from rest_framework.views import APIView # -> for class API view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from IOT.models import User, UserProfile, Sensor, SensorValueStore, Notification
from IOT.serializers import UserProfileCreateSerializer, UserProfileSerializer, SensorSerializer
from IOT.permissions import FullDjangoModelPermissions, AdminOnlyRead

# Create your views here.

def all_users(request):
    
    query_set = User.objects.all()
    #query_set = query_set[5:10]
    
    return render(request, 'check.html', {'results': list(query_set)})



def count_users(request):
    
    query_set = User.objects.count()
    
    return render(request, 'check.html', {'results': query_set})



def particular_users(request):
    
    #query_set = User.objects.get(id=0) #(pk=0)
    #query_set = User.objects.filter(id=0)
    #query_set = User.objects.filter(id=0).first()
    query_set = User.objects.filter(id=4).exists()
    
    return render(request, 'check.html', {'results': list(query_set)})

    # .first() if exists returns first data, if does not exist return none
    # .exists() we get boolean value if the data exists or not



def filtering_sensors(request):
    
    #query_set = Sensor.objects.filter(value__lt=30) #range=(20,30), gt=40
    query_set = Sensor.objects.filter(name__icontains='TemPeraTure') #contains='temperature' -> case sensative

    return render(request, 'check.html', {'results': list(query_set)})

    #for date and time field: update__year=sth, update__date=sth
    #checking for null value: title__isnull=True
    


def user_sensor_filter(request):
    
    query_set = Sensor.objects.filter(user__id__range=(3, 7))
    
    return render(request, 'check.html', {'results': list(query_set)})



def many_condition_filter(request):
    
    #query_set = Sensor.objects.filter(user__id__range=(3, 7), name__icontains='TemPeraTure')
    query_set = Sensor.objects.filter(user__id__range=(3, 7)).filter(name__icontains='TemPeraTure')
    
    return render(request, 'check.html', {'results': list(query_set)})



def q_f_objects(request):
    
    #query_set = Sensor.objects.filter(Q(user__id__range=(3, 7)) & Q(name__icontains='TemPeraTure')) # or -> |, not -> ~
    #query_set = Sensor.objects.filter(value=23*F('id'))
    #query_set = Sensor.objects.filter(value=11*F('user__id'))
    query_set = SensorValueStore.objects.filter(value=7.5*F('sensor__user__id'))
    
    return render(request, 'check.html', {'results': list(query_set)})



def sorting(request):
    
    #query_set = Notification.objects.order_by('name')
    #query_set = Notification.objects.order_by('-name')
    #query_set = Notification.objects.order_by('name', '-text') #if same name, sort by descending order of text
    #query_set = Notification.objects.order_by('name', '-text').reverse()[0] 
    #query_set = Notification.objects.earliest('name') #sort and get first object
    query_set = Notification.objects.latest('name')

    return render(request, 'check.html', {'results': query_set}) #list(query_set)

    #note: use order_by method after filter method
        #only return query_set in html in [0], earliest, latest



def selecting_field(request):
    
    #query_set = Sensor.objects.all().values('id', 'name', 'user__username') #gives dictionaries
    #query_set = Sensor.objects.values_list('name', 'user__username') #gives touples
    #query_set = Sensor.objects.values('name', 'user__username').distinct() #removes duplicate {name, user__username} if exists

    #get all the sensor for the given selected user query_set
    query_set_user = User.objects.filter(id=7).values('id')
    query_set = Sensor.objects.filter(user__id__in=query_set_user).values('id', 'name').order_by('name')

    #the worst method .only and .defer !!don't use until it is very necessary. So I didn't mention here

    return render(request, 'check.html', {'results': list(query_set)})



def selecting_related_objects(request):
    
    #select_related is used if a sensor has only one user
    #query_set = Sensor.objects.select_related('user').all() #if we want to use sensor.user.id, it is efficient to load earlier
    #query_set = Sensor.objects.select_related('user__rfid').all() #the sensor that has one user that has one rfid
    
    #prefetch_releated is used if same sensor has multiple values store
    #query_set = Sensor.objects.prefetch_related('user').filter(id__lt=2) #select one user where that sensor id is 2
    #query_set = Sensor.objects.prefetch_related('sensorvaluestore_set').filter(id__lt=4) #loading group of set for one sensor requires "_set"
    #query_set = User.objects.prefetch_related('sensor_set__sensorvaluestore_set').all() #relation of sensor to sensorvaluestore to sensor that has multiple sets
    query_set = Sensor.objects.select_related('user').prefetch_related('sensorvaluestore_set').filter(id__lt=4) #mixed

    return render(request, 'check.html', {'results': list(query_set)})

    #note: you can chain selected_related and prefetch_related to make complex queries
        #select_related is used for getting many-one, one-one
        #prefetch_related is used for getting one-many, many-many


###################################################################################################################


class UserProfileCreate(ListCreateAPIView):

    permission_classes = [FullDjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        return UserProfileCreateSerializer

    def get(self, request):
        query_set = get_object_or_404(UserProfile.objects.filter(user_id=request.user.id))
        serializer = UserProfileCreateSerializer(query_set)
        return Response(serializer.data)
    
    def post(self, request):
        print(request.data)
        serializer = UserProfileCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(request.user.id) != str(request.data['user']):
            return Response({"detail":"user cannot be changed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



class UserProfileDetail(RetrieveUpdateDestroyAPIView):

    http_method_names = ['get', 'put', 'delete', 'head', 'options']
    permission_classes = [FullDjangoModelPermissions, IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        return UserProfileSerializer

    def get(self, request):
        query_set = get_object_or_404(UserProfile.objects.filter(user_id=request.user.id))
        serializer = UserProfileSerializer(query_set)
        return Response(serializer.data)
    
    def put(self, request):
        query_set = get_object_or_404(UserProfile.objects.filter(user_id=request.user.id))
        serializer = UserProfileSerializer(query_set, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    
    def delete(self, request):
        query_set = get_object_or_404(UserProfile.objects.filter(user_id=request.user.id))
        query_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
class SensorList(ListAPIView):

    permission_classes = [FullDjangoModelPermissions]#, AdminOnlyRead]

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
    
    #we can define methods as we like inside generic view class
    """
    def get(self, request):
        query_set = Sensor.objects.select_related('user').all()
        serializer = SensorSerializer(query_set, many=True, context={'request': request})
        return Response(serializer.data)
    
        #context={'request': request} is for hyperlink generation of parent object #doesnot required in generic view XD
    
    def post(self, request):
        serializer = SensorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    """ 



class UserSensorList(ListCreateAPIView):

    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        queryset = Sensor.objects.select_related('user').filter(user__pk=user_pk)
        return queryset
    
    def get_serializer_class(self):
        return SensorSerializer
    
    

class UserSensorDetail(RetrieveDestroyAPIView):

    def get_queryset(self):
        user_pk = self.kwargs['user_pk']
        pk = self.kwargs['pk']
        queryset = Sensor.objects.select_related('user').filter(user__pk=user_pk).filter(pk=pk)
        return queryset
    
    # in RetrieveUpdateDestroyAPIView, we don't need to use get_object_or_404, 
    # ->filter will return error msg instead of empty list
    
    def get_serializer_class(self):
        return SensorSerializer
    
    #restricting user change for given sensor
    def put(self, request, user_pk, pk):
        query_set = get_object_or_404(Sensor.objects.select_related('user').filter(user__pk=user_pk), pk=pk)
        serializer = SensorSerializer(query_set, data=request.data)
        serializer.is_valid(raise_exception=True)
        if str(user_pk) != str(request.data['user']):
            return Response({"detail":"user cannot be changed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



#generic view for SensorDetail
class SensorDetail(RetrieveDestroyAPIView):

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = Sensor.objects.select_related('user').filter(pk=pk)
        return queryset
    
    def get_serializer_class(self):
        return SensorSerializer
    
    def put(self, request, pk):
        query_set = get_object_or_404(Sensor.objects.select_related('user'), pk=pk)
        serializer = SensorSerializer(query_set, data=request.data)
        serializer.is_valid(raise_exception=True)
        print(query_set.user.pk, request.data['user'])
        if str(query_set.user.pk) != str(request.data['user']):
            return Response({"detail":"user cannot be changed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    #we can define methods as we like inside generic view class
    """
    def get(self, request, pk):
        #query_set = Sensor.objects.get(pk=id) #404 error not handled
        query_set = get_object_or_404(Sensor, pk=pk)
        serializer = SensorSerializer(query_set)
        return Response(serializer.data)

    def delete(self, request, pk):
        query_set = get_object_or_404(Sensor, pk=pk)
        query_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    """