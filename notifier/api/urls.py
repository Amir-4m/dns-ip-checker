from django.urls import path
from .views import NotifierApiView

urlpatterns = [
    path('send/', NotifierApiView.as_view(), name="notifier-send"),
]
