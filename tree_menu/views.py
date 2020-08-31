from django.shortcuts import render

from .models import Menu, MenuItem




def index(request):
    return render(request, 'tree_menu/index.html')

def any_page(request, slug):
    return render(request, 'tree_menu/index.html')