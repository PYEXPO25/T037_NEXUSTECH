from django.urls import path
from . import views

app_name = 'attendance_records'


urlpatterns = [
    path('', views.login_view, name='log_in'),
    path('index/',views.index,name = 'index'),
]                                                                  