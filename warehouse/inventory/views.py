
# Create your views here.
from django.http import JsonResponse
from .models import Item
from django.shortcuts import get_object_or_404,  render, redirect
from .forms import ItemForm
from .models import Item
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if item_id:
            item = get_object_or_404(Item, id=item_id)
            form = ItemForm(request.POST, instance=item)
        else:
            form = ItemForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('index')

    else:
        form = ItemForm()

    items = Item.objects.all()
    return render(request, 'inventory/index.html', {'form': form, 'items': items})

def get_items(request):
    items = list(Item.objects.values())
    return JsonResponse({'items': items})


@csrf_exempt
def order_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if item.in_stock > 0:
        item.in_stock -= 1
        item.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failure', 'message': 'Out of stock'})
