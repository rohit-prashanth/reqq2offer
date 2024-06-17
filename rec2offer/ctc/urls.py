from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # API endpoints related to views that are currently active
    # path('employee-get/', views.HrTeamView.as_view(), name='employee_list'),
    # path('employee-get/<str:id>/', views.HrTeamView.as_view(), name='employee_detail'),
    # path('create-offer-letter/', views.CreateOfferLetter.as_view(), name='employee_detail'),

    path('create-column/', views.ColumnCreationAPIView.as_view(), name='create-column'),
    path('add-dummydata/', views.DummyDataAPIView.as_view(), name='add-dummydata'),
    path('get-dummydata/', views.DummyDataAPIView.as_view(), name='get-dummydata'),
    path('del-dummydata/<field_name>/', views.DeleteFieldAPIView.as_view(), name='del-dummydata'),
]
    # Uncomment and properly import the following views if they are implemented
   
    # path('dropdowndata/', views.CheckboxApiView.as_view(), name='dropdown'),

    # Example of uncommenting and importing views:
    # path('logout/', views.Userlogout.as_view(), name='user_logout'),
    # path('view-user/', views.ViewUser.as_view(), name='view_user'),
    # path('create-user/', views.UserCreate.as_view(), name='create_user'),
    # path('user/<int:id>/', views.GetId.as_view(), name='get_user'),

