from django.urls import path
from IOT import views

urlpatterns = [
    path('all_users/', views.all_users),
    path('count_users/', views.count_users),
    path('particular_users/', views.particular_users),
    path('filtering_sensors/', views.filtering_sensors),
    path('user_sensor_filter/', views.user_sensor_filter),
    path('many_condition_filter/', views.many_condition_filter),
    path('q_f_objects/', views.q_f_objects),
    path('sorting/', views.sorting),
    path('selecting_field/', views.selecting_field),
    path('selecting_related_objects/', views.selecting_related_objects),

    #############################################################################

    path('userprofiles/', views.UserProfileCreate.as_view(), name = 'UserProfileCreate'),
    path('userprofiles/me/', views.UserProfileDetail.as_view(), name = 'UserProfileDetail'),

    path('sensors/', views.SensorList.as_view(), name = 'SensorList'),

    #path('sensors/<int:pk>/', views.SensorDetail.as_view(), name = 'SensorDetail'),

    #path('users/<int:user_pk>/sensors/', views.UserSensorList.as_view(), name = 'UserSensorList'),
    #path('users/<int:user_pk>/sensors/<int:pk>/', views.UserSensorDetail.as_view(), name = 'UserSensorDetail'),

]