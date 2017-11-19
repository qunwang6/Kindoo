from django.conf.urls import url
from .views import viewBook

urlpatterns = [
    url(r'^list/', viewBook),
]
