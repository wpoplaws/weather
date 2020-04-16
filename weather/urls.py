from django.urls import path
from . import views

urlpatterns = [
    path('forecast/', views.forecast, name='forecast'),
    path('no_data/', views.no_data, name='no_data'),

    path('', views.main, name='main'),

]
