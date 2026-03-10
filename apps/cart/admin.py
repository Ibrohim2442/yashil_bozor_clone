from django.contrib import admin

from apps.cart.models import Cart, CartItem

# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ("product",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "items_count", "created_at", "updated_at")
    search_fields = ("user__phone", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")
    inlines = (CartItemInline,)

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = "Items"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity", "updated_at")
    list_filter = ("updated_at",)
    search_fields = ("product__name", "cart__user__phone")
    autocomplete_fields = ("product", "cart")

    def has_add_permission(self, request):
        return False

    def has_edit_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False