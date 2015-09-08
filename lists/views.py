from django.shortcuts import render, redirect

from .models import Item, List


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['new_item_text'])
        return redirect('/lists/the-only-list')

    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list/')
