from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.Userlogin.as_view(), name='userlogin'),
    path('logout/', views.Userlogout.as_view(), name='userlogout'),
    path('view-user/', views.ViewUser.as_view(), name='view-user'),
    path('create-user/', views.UserCreate.as_view(), name='create-user'),
    path('user/<int:id>/', views.GetId.as_view(), name='get_user'),  # Ensure Get_id is properly imported
]
