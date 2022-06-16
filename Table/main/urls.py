from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(views.TablePage), name='home'),
    path('time', csrf_exempt(views.TimeTablePage), name='time'),
    path('manual', csrf_exempt(views.ManualPage), name='manual'),
    path('api', csrf_exempt(views.api), name='api'),
]
