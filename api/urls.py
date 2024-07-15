from django.urls import path
from . import views
from .views import delete_status, get_owner, receive_status, get_status, receive_plate, get_plate, receive_owner

urlpatterns = [
    path('owners/', get_owner, name='get_owner'),
    path('status/', get_status, name='get_status'),
    path('receive-status/', receive_status, name='post_status'),
    path('delete_status/', delete_status, name='delete_status'),
    path('receive-plate/', receive_plate, name='post_status'),
    path('plate/', get_plate, name='get_plate'),
    path('receive-owner/', receive_owner, name='post_owner')



]
