from django.urls import path
from .views import NotifierApiView

urlpatterns = [
    path('', NotifierApiView.as_view(), name="notifier-api"),
]
