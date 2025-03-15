from . import views
from django.urls import path

urlpatterns=[
    path('ph/',views.print_hello)
]