from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm

# 1. READ (List all items)
def item_list(request):
    items = Item.objects.all()
    return render(request, 'inventory/item_list.html', {'items': items})

# 2. CREATE
def item_create(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('item_list')
    return render(request, 'inventory/item_form.html', {'form': form})

# 3. UPDATE
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('item_list')
    return render(request, 'inventory/item_form.html', {'form': form})

# 4. DELETE
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

from rest_framework import viewsets
from .serializers import ItemSerializer

# This single ViewSet handles List, Create, Retrieve, Update, and Destroy automatically!
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
