
from django.urls import path
from . import views
from .views import team_portfolio

app_name = 'attendance_records'


urlpatterns = [
    path('', views.login_view, name='login'),
    path('index/', views.index_view, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('take_attendance/',views.take_attendance,name='take_attendance'), 
    path('team-portfolio/', team_portfolio, name='team-portfolio'),
]                                                                  