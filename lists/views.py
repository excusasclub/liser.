from django.shortcuts import render, get_object_or_404
from .models import BagList
from accounts.models import Profile

def baglist_detail(request, handle, slug):
    # Buscamos el perfil por handle
    profile = get_object_or_404(Profile, handle=handle)
    
    # Buscamos la BagList por slug y owner
    baglist = get_object_or_404(BagList, owner=profile, slug=slug)
    
    return render(request, 'lists/baglist_detail.html', {'baglist': baglist})


