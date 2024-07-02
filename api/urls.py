from django.urls import path
from . import views
from .views import get_owner, receive_status, get_status

urlpatterns = [
    # path('save-crop/', receive_crop, name='save_image'),
    path('owners/', get_owner, name='get_owner'),
    path('receive-status/', receive_status, name='receive_status'),
    path('status/', get_status, name='get_status')



]
