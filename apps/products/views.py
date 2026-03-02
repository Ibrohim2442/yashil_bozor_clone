from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.products.filters import ProductFilter
from apps.products.models import Product
from apps.products.serialzier import ProductSerializer


# Create your views here.

class CategoryProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [OrderingFilter]
    filterset_class = ProductFilter

    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        # return Product.objects.filter(category_id=category_id)
        return (
            Product.objects
            .select_related("seller", "category")
            .prefetch_related("images")
            .filter(category_id=category_id)
        )