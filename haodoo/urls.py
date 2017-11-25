from django.conf.urls import url
from .views import formHandler

urlpatterns = [
    url("", formHandler),
]
