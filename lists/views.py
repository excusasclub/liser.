from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from .models import BagList
from .forms import BagListForm
from accounts.models import Profile

def baglist_detail(request, handle, slug):
    """
    Vista de solo lectura de una BagList.
    """
    # Buscamos el perfil por handle
    profile = get_object_or_404(Profile, handle=handle)
    
    # Buscamos la BagList por slug y owner
    baglist = get_object_or_404(BagList, owner=profile, slug=slug)
    
    return render(request, 'lists/baglist_detail.html', {'baglist': baglist})


@login_required
def baglist_edit(request, handle, slug):
    """
    Vista para editar una BagList.
    Solo accesible por el owner de la lista.
    """
    # Buscamos el perfil del owner
    profile = get_object_or_404(Profile, handle=handle)

    # Buscamos la BagList que se va a editar
    baglist = get_object_or_404(BagList, owner=profile, slug=slug)

    # Solo el owner puede editar
    if request.user.profile != profile:
        return redirect('lists:baglist_detail', handle=handle, slug=slug)

    if request.method == 'POST':
        form = BagListForm(request.POST, instance=baglist)
        if form.is_valid():
            form.save()
            return redirect('lists:baglist_detail', handle=baglist.owner.handle, slug=baglist.slug)

  
    else:
        form = BagListForm(instance=baglist)

    return render(request, 'lists/baglist_edit.html', {
        'baglist': baglist,
        'form': form
    })


@login_required
def baglist_create(request):
    """
    Vista para crear una nueva BagList.
    """
    if request.method == 'POST':
        form = BagListForm(request.POST)
        if form.is_valid():
            baglist = form.save(commit=False)
            baglist.owner = request.user.profile
            
            # Generar slug único para este usuario
            base_slug = slugify(baglist.title)
            if not base_slug:
                base_slug = "untitled"
            
            slug = base_slug
            counter = 1
            while BagList.objects.filter(owner=baglist.owner, slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            baglist.slug = slug
            
            baglist.save()
            messages.success(request, "BagList creada exitosamente.")
            # Redirigir al editor
            return redirect('lists:baglist_edit', handle=baglist.owner.handle, slug=baglist.slug)
    else:
        form = BagListForm()

    return render(request, 'lists/baglist_create.html', {'form': form})


@login_required
def dashboard(request):
    """
    Dashboard principal del usuario. Muestra sus BagLists.
    """
    baglists = BagList.objects.filter(owner=request.user.profile, is_deleted=False).order_by("-updated_at")
    return render(request, 'lists/dashboard.html', {'baglists': baglists})
