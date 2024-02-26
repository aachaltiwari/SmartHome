
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer

from IOT.models import  UserProfile, Sensor



class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']



class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']



class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'phone_no']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_id', 'phone_no']

    user_id = serializers.IntegerField(read_only=True)
    
    
    
    

class SensorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sensor
        fields = ['pk', 'name', 'value', 'say_hello', 'user']#, 'username']
        #fields = '__all__' -> this is bad to expose all information

    #username = serializers.CharField(source='user.username', read_only=True)

    #if ModelSerializer is not used
    #pk = serializers.IntegerField()
    #name = serializers.CharField(max_length=255)
    #value = serializers.FloatField()

    #you can edit user (parent) object in 3 ways:
    #user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    #user = UserSerializer() #you can add many=True if multiple user
    #user = serializers.HyperlinkedRelatedField(queryset=User.objects.all(), view_name='UserDetail')
    
    #new field
    say_hello = serializers.SerializerMethodField(method_name='hello')

    def hello(self, sensor: Sensor):
        return f'Hello {sensor.value}'





