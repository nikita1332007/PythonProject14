from datetime import datetime

from django.shortcuts import render, get_object_or_404

from catalog.models import Product


def home_view(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products, 'year': datetime.now().year})

def contacts_view(request):
    success_message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        success_message = "Спасибо! Ваше сообщение отправлено."
    return render(request, 'catalog/contacts.html', {'success_message': success_message, 'year': datetime.now().year})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product, 'year': datetime.now().year})