from django.urls import path
from . import views
from . import views_htmx

app_name = "lists"

urlpatterns = [
    path("baglist/<str:handle>/<slug:slug>/", views.baglist_detail, name="baglist_detail"),
    path("baglist/<str:handle>/<slug:slug>/edit/", views.baglist_edit, name="baglist_edit"),
    path("editor/", views_htmx.htmx_editor, name="baglist_editor"),
    path("htmx/baglist-sections/", views_htmx.htmx_baglist_sections, name="htmx_baglist_sections"),
    path("htmx/item-picker/", views_htmx.htmx_item_picker, name="htmx_item_picker"),
    path("htmx/update-section-title/", views_htmx.htmx_update_section_title, name="htmx_update_section_title"),

]
