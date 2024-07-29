from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('browse_captions/', views.browse_captions, name='browse_captions'),
    path('like_image/<int:image_caption_id>/', views.like_image, name='like_image'),
]
