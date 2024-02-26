from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass



class UserProfile(models.Model):
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)



class RFID(models.Model):
    door_status = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def str(self):
        return f'{self.door_status}'



class Wifi(models.Model):
    wifi_ssid = models.CharField(max_length=255)
    wifi_password = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def str(self):
        return f'{self.wifi_ssid}'



class Notification(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def str(self):
        return f'{self.name}'



class Room(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def str(self):
       return f'{self.name}'



class Sensor(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def str(self):
        return f'{self.name}'



class Bulb(models.Model):
    colour = models.CharField(max_length=255)
    bulb_status = models.BooleanField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)



class SensorValueStore(models.Model):
    value = models.FloatField()
    date = models.DateTimeField(auto_now_add = True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)