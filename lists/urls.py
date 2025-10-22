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
    path("htmx/delete-section/", views_htmx.htmx_delete_section, name="htmx_delete_section"),
    path("htmx/remove-item-from-section/", views_htmx.htmx_remove_item_from_section, name="htmx_remove_item_from_section"),
    path("htmx/update-section-description/", views_htmx.htmx_update_section_description, name="htmx_update_section_description"),
    path("htmx/update-section-position/", views_htmx.htmx_update_section_position, name="htmx_update_section_position"),
    path("add-item-to-section/", views_htmx.htmx_add_item_to_section, name="htmx_add_item_to_section"),
]
