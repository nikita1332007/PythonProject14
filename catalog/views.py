from django.shortcuts import render

def home_view(request):
    return render(request, 'catalog/home.html')

def contacts_view(request):
    success_message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        success_message = "Спасибо! Ваше сообщение отправлено."
    return render(request, 'catalog/contacts.html', {'success_message': success_message})