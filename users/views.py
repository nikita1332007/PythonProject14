from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

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

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'product_list'
