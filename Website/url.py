from django.urls import path, include
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path('', include('myapp.urls')),
]
