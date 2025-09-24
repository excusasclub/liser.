# liser2/urls.py
from django.contrib import admin
from django.urls import path, include
from lists import views as lists_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Ruta para ver una BagList usando handle + slug
    path('<str:handle>/baglist/<slug:slug>/', lists_views.baglist_detail, name='baglist_detail'),

    # Si tienes otras rutas de la app lists
    path('', include('lists.urls', namespace='lists')),
]

