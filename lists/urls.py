from django.urls import path
from . import views

app_name = 'lists'

urlpatterns = [
    path('baglist/<str:handle>/<slug:slug>/', views.baglist_detail, name='baglist_detail'),
]