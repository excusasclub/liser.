from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import BagList, BagListSection


@login_required
def htmx_editor(request):
    """Vista principal del editor HTMX de BagLists."""
    baglists = BagList.objects.filter(owner=request.user.profile, is_deleted=False).order_by("title")
    return render(request, "lists/baglist_edit_htmx.html", {"baglists": baglists})


@login_required
def htmx_baglist_sections(request):
    """Carga todas las secciones de una BagList seleccionada (HTMX)."""
    baglist_id = request.GET.get("baglist_id")
    baglist = get_object_or_404(BagList, id=baglist_id, owner=request.user.profile)
    return render(request, "partials/baglist_sections_list.html", {"baglist": baglist})


@login_required
def htmx_item_picker(request):
    """Placeholder temporal para el selector de items."""
    return HttpResponse("<div class='p-4 bg-white border rounded'>Item picker en construcción</div>")


@login_required
def htmx_update_section_title(request):
    """Actualiza el título de una subBagList (sección) vía HTMX."""
    if request.method == "POST":
        section_id = request.POST.get("section_id")
        title = request.POST.get("title", "").strip()

        # Verificar que la sección pertenece al usuario
        section = BagListSection.objects.filter(
            id=section_id, baglist__owner=request.user.profile
        ).first()
        if not section:
            return JsonResponse({"success": False, "error": "Sección no encontrada"}, status=404)

        section.title = title
        section.save(update_fields=["title"])
        return JsonResponse({"success": True, "title": title})

    return JsonResponse({"success": False, "error": "Método inválido"}, status=400)
