from django.urls import path
from . import views

app_name = 'lists'

urlpatterns = [
    path('baglist/<int:pk>/', views.baglist_detail, name='baglist_detail'),
]
