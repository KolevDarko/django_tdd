from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['new_item_text'])
        return redirect('/lists/the-only-list')

    return render(request, 'home.html')


def view_list(request, list_id):
    items = Item.objects.filter(list=list_id).all()
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'items': items, 'list': list_})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id))


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id))
