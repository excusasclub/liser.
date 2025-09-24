from django.urls import path
from . import views

app_name = 'lists'

urlpatterns = [
    path('baglist/<uuid:baglist_id>/', views.baglist_detail, name='baglist_detail'),
]
