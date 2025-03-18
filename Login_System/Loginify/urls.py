from . import views
from django.urls import path

urlpatterns=[
    path('ph/',views.print_hello),
    path('home/',views.home_page),
    path('signup/',views.signup),
    path('login/',views.login),
    path('create/', views.create_user),
    path('get_users/', views.get_all_users),
    path('user_by_email/<str:email>/', views.get_user_by_email),
    path('update_user/<str:email>/', views.update_user_data),
    path('delete_user/<str:email>/', views.delete_user_data)
]