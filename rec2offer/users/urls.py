from django.contrib import admin
from django.urls import path, include
from . import views
from rec2offer import settings 
from django.conf.urls.static import static
from .views import UploadImageView

urlpatterns = [
    path('login/', views.Userlogin.as_view(), name='userlogin'),
    path('logout/', views.Userlogout.as_view(), name='userlogout'),
    path('view-user/', views.ViewUser.as_view(), name='view-user'),
    path('create-user/', views.UserCreate.as_view(), name='create-user'),
    path('user/<int:id>/', views.GetId.as_view(), name='get_user'),  # Ensure Get_id is properly imported
    # urls.py



    path('upload/', UploadImageView.as_view(), name='upload_image'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
