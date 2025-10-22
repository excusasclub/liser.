from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import BagList, BagListSection, BagListItem


# === Editor principal ===
@login_required
def htmx_editor(request):
    """Vista principal del editor HTMX de BagLists."""
    baglists = BagList.objects.filter(owner=request.user.profile, is_deleted=False).order_by("title")
    return render(request, "lists/baglist_edit_htmx.html", {"baglists": baglists})


# === Secciones (subBagLists) ===
@login_required
def htmx_baglist_sections(request):
    """Carga todas las secciones de una BagList seleccionada (HTMX)."""
    baglist_id = request.GET.get("baglist_id")
    baglist = get_object_or_404(BagList, id=baglist_id, owner=request.user.profile)
    return render(request, "partials/baglist_sections_list.html", {"baglist": baglist})


# === Item Picker ===
@login_required
def htmx_item_picker(request):
    """Muestra un listado rápido de items del usuario para asociar a una subBagList."""
    section_id = request.GET.get("section_id")
    profile = request.user.profile

    # Filtra los últimos 30 items del usuario
    user_items = (
        BagListItem.objects
        .filter(baglist__owner=profile)
        .select_related("snapshot")
        .order_by("-created_at")[:30]
    )

    return render(request, "partials/item_picker_modal.html", {
        "user_items": user_items,
        "active_section_id": section_id,
    })
@login_required
def htmx_add_item_to_section(request):
    """Asocia un item existente a una sección concreta."""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Método inválido"}, status=400)

    section_id = request.POST.get("section_id")
    item_id = request.POST.get("item_id")

    # Validar pertenencia al usuario
    item = BagListItem.objects.filter(
        id=item_id,
        baglist__owner=request.user.profile
    ).first()

    section = BagListSection.objects.filter(
        id=section_id,
        baglist__owner=request.user.profile
    ).first()

    if not item or not section:
        return JsonResponse({"success": False, "error": "Item o sección no encontrados"}, status=404)

    item.section = section
    item.save(update_fields=["section"])

    return JsonResponse({"success": True})



# === Actualizar título de sección ===
@login_required
def htmx_update_section_title(request):
    """Actualiza el título de una subBagList (sección) vía HTMX."""
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        title = request.POST.get("title", "").strip()

        section = BagListSection.objects.filter(
            id=section_id, baglist__owner=request.user.profile
        ).first()
        if not section:
            return JsonResponse({"success": False, "error": "Sección no encontrada"}, status=404)

        section.title = title
        section.save(update_fields=["title"])
        return JsonResponse({"success": True, "title": title})

    return JsonResponse({"success": False, "error": "Método inválido"}, status=400)


# === Eliminar sección ===
@login_required
def htmx_delete_section(request):
    """Elimina una sección (solo la sección, no los items)."""
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        section = get_object_or_404(BagListSection, id=section_id, baglist__owner=request.user.profile)
        section.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"})


# === Actualizar descripción ===
@login_required
def htmx_update_section_description(request):
    """Actualiza la descripción de una subBagList."""
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        desc = request.POST.get("description", "")
        section = get_object_or_404(BagListSection, id=section_id, baglist__owner=request.user.profile)
        section.description = desc
        section.save(update_fields=["description"])
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"})


# === Actualizar posición ===
@login_required
def htmx_update_section_position(request):
    """Actualiza la posición de una sección."""
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        pos = request.POST.get("position")
        section = get_object_or_404(BagListSection, id=section_id, baglist__owner=request.user.profile)
        section.position = pos or 0
        section.save(update_fields=["position"])
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"})


# === Desasociar item de una sección ===
@login_required
def htmx_remove_item_from_section(request):
    """Desasocia un item de su sección (no lo elimina del usuario)."""
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Método inválido"}, status=400)

    section_id = request.POST.get("section_id")
    item_id = request.POST.get("item_id")

    item = BagListItem.objects.filter(
        id=item_id,
        baglist__owner=request.user.profile,
        section_id=section_id
    ).first()

    if not item:
        return JsonResponse({"success": False, "error": "Item no encontrado"}, status=404)

    item.section = None
    item.save(update_fields=["section"])

    return JsonResponse({"success": True})
