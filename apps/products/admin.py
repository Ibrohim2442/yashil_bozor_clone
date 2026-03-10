from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.html import format_html

from apps.products.models import Product, ProductImage, Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ProductImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        images = [
            form.cleaned_data
            for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        ]

        if not images:
            raise ValidationError("At least one image is required.")

        main_images = [img for img in images if img.get("is_main")]

        if not main_images:
            if len(images) == 1:
                images[0]["is_main"] = True
            else:
                raise ValidationError("At least one image must be marked as main.")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    formset = ProductImageInlineFormSet
    extra = 1
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="object-fit:contain;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "seller",
        "price",
        "discount_price",
        "stock",
        "in_stock",
    )
    list_filter = ("category", "seller", "height", "care", "light")
    search_fields = ("name", "description")
    inlines = (ProductImageInline,)

    def in_stock(self, obj):
        return obj.stock > 0
    in_stock.boolean = True
    in_stock.short_description = "In Stock"