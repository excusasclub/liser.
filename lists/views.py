from django.shortcuts import render, get_object_or_404
from .models import BagList

def baglist_detail(request, pk):
    baglist = get_object_or_404(BagList, pk=pk)
    return render(request, 'lists/baglist_detail.html', {'baglist': baglist})
