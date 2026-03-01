from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ['price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipient_name', 'total_price', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['recipient_name', 'recipient_phone']
    readonly_fields = ['total_price', 'created_at']
    inlines = [OrderItemInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if hasattr(instance, 'product') and not instance.price:
                instance.price = instance.product.price
            instance.save()
        formset.save_m2m()

        order = form.instance
        order.total_price = sum(item.price * item.quantity for item in order.items.all())
        order.save(update_fields=['total_price'])


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    readonly_fields = ['price']