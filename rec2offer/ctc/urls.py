from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('employee-get/', views.HrTeamView.as_view(), name='employee_list'),
    path('employee-get/<str:id>/', views.HrTeamView.as_view(), name='employee_detail'),
    # Uncomment and properly import the following views if they are implemented
    # path('logout/', views.Userlogout.as_view(), name='user_logout'),
    # path('view-user/', views.ViewUser.as_view(), name='view_user'),
    # path('create-user/', views.UserCreate.as_view(), name='create_user'),
    # path('user/<int:id>/', views.GetId.as_view(), name='get_user'),
]
