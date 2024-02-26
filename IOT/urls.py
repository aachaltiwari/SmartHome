from django.urls import path
from IOT import views

urlpatterns = [
    path('userprofiles/', views.UserProfileCreate.as_view(), name = 'UserProfileCreate'),
    path('userprofiles/me/', views.UserProfileDetail.as_view(), name = 'UserProfileDetail'),
    path('sensors/', views.SensorList.as_view(), name = 'SensorList'),
    path('sensors/<int:pk>/', views.SensorDetail.as_view(), name = 'SensorDetail'),
]