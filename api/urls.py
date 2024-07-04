from django.urls import path
from . import views
from .views import get_owner, receive_status, get_status

urlpatterns = [
    path('owners/', get_owner, name='get_owner'),
    path('status/', get_status, name='get_status'),
    path('receive-status/', receive_status, name='post_status')


]
