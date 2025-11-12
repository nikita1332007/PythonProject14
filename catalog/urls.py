from django.urls import path
from .views import HomeView, ContactView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]