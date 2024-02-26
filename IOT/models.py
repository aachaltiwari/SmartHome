from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)



class RFID(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    door_status = models.BooleanField()

    def __str__(self):
        return f'{self.door_status}'


class Wifi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    wifi_ssid = models.CharField(max_length=255)
    wifi_password = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.wifi_ssid}'


class Notification(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
       return f'{self.name}'


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name}'


class Bulb(models.Model):
    colour = models.CharField(max_length=255)
    bulb_status = models.BooleanField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)


class SensorValueStore(models.Model):
    value = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)


