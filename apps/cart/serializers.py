from rest_framework import serializers

from apps.cart.models import Cart, CartItem
from apps.products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(
        source='product.price', max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ('id', 'product_id', 'product_name', 'price', 'quantity')

    def validate(self, attrs):
        product_id = attrs.get("product_id")
        quantity = attrs.get("quantity", 1)

        product = Product.objects.filter(id=product_id).first()
        if not product:
            raise serializers.ValidationError("Product not found.")

        if not product.is_in_stock:
            raise serializers.ValidationError("Product is out of stock.")

        if quantity > product.stock:
            raise serializers.ValidationError("Not enough stock.")

        return attrs

    def create(self, validated_data):
        cart = self.context['cart']
        product_id = validated_data.pop('product_id')
        quantity = validated_data.get('quantity', 1)
        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product = product,
            defaults={"quantity": quantity},
        )

        if not created:
            item.quantity += quantity
            item.save()

        return item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'items', 'total_price')

    def get_total_price(self, obj):
        total = 0
        for item in obj.items.all():
            effective_price = item.product.discount_price or item.product.price
            total += effective_price * item.quantity
        return total