from django.core.mail import send_mail

def form_valid(self, form):
    response = super().form_valid(form)
    user_email = form.cleaned_data.get('email')
    send_mail(
        'Добро пожаловать',
        'Спасибо за регистрацию!',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )
    return response
