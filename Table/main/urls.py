from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', csrf_exempt(views.TablePage), name='home'),
    path('api', csrf_exempt(views.api), name='api'),
]
