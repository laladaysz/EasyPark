from django.urls import path
from . import views
from .views import receive_crop

urlpatterns = [
    path('save-crop/', receive_crop, name='save_image'),
    
]
