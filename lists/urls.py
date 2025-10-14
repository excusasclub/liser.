from django.urls import path
from . import views

app_name = 'lists'

urlpatterns = [
    path('baglist/<str:handle>/<slug:slug>/', views.baglist_detail, name='baglist_detail'),
        # Edición de BagList
    path('baglist/<str:handle>/<slug:slug>/edit/', views.baglist_edit, name='baglist_edit'),

]