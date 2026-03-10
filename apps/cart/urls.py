from django.urls import path
from apps.cart.views import CartDetailView, AddToCartView, CartItemDetail

urlpatterns = [
    path("", CartDetailView.as_view()),
    path("items/", AddToCartView.as_view()),
    path("items/<int:pk>/", CartItemDetail.as_view()),
]