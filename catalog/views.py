from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from datetime import datetime
from catalog.models import Product
from catalog.forms import ProductForm

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

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user

    def handle_no_permission(self):
        return HttpResponseForbidden('Только владелец может редактировать продукт.')

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        is_moderator = user.groups.filter(name='Модератор продуктов').exists()
        return product.owner == user or is_moderator

    def handle_no_permission(self):
        return HttpResponseForbidden('Удалять продукт можно только владельцу или модератору.')

@login_required
def unpublish_product(request, product_id):
    if not request.user.has_perm('catalog.can_unpublish_product'):
        return HttpResponseForbidden('Нет прав на отмену публикации.')
    product = get_object_or_404(Product, id=product_id)
    product.status = 'draft'
    product.save()
    return redirect('product_detail', pk=product.id)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    is_moderator = user.groups.filter(name='Модератор продуктов').exists()
    if product.owner != user and not is_moderator:
        return HttpResponseForbidden('Удалять продукт можно только владельцу или модератору.')
    product.delete()
    return redirect('product_list')