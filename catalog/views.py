from django.views.generic import TemplateView, DetailView
from datetime import datetime
from catalog.models import Product


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['year'] = datetime.now().year
        return context


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_message'] = None
        context['year'] = datetime.now().year
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['success_message'] = "Спасибо! Ваше сообщение отправлено."
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = datetime.now().year
        return context