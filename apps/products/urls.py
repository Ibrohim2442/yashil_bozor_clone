from django.urls import path
from .views import CategoryProductsView

urlpatterns = [
    path("categories/<int:category_id>/", CategoryProductsView.as_view()),
]