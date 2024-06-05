from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:id>/', views.get_user, name='get_user'),
]