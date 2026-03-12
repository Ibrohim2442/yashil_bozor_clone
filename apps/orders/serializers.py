from django.template.context_processors import request
from rest_framework import serializers
from .models import Order, OrderItem, OrderItemReview
from ..products.serializers import ProductSerializer


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['price']

class OrderItemReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemReview
        fields = ['order_item', 'rating', 'pros', 'cons', 'comment', 'created_at']

    def validate(self, data): # what is inside request
        request = self.context['request']
        user = request.user
        # order = data.get('order')

        order_item = data.get('order_item')

        order = order_item.order
        print(order.user, user)
        # The order belong to the exact user who ordered
        if order.user != user:
            raise serializers.ValidationError('The order you want review not belong to you')

        # The status of order should be delivered
        if order.status != 'delivered':
            raise serializers.ValidationError('The order not delivered to you')

        return data

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'recipient_name',
            'recipient_phone',
            'courier_note',
            'address',
            'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data, user=self.context['request'].user, total_price=0)

        total = 0
        for item in items_data:
            price = item['product'].price
            OrderItem.objects.create(order=order, price=price, **item)
            total += price * item['quantity']

        order.total_price = total
        order.save()
        return order

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'recipient_name', 'recipient_phone',
            'courier_note', 'address', 'total_price',
            'status', 'items', 'created_at'
        ]
        read_only_fields = ['total_price', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data, user=self.context['request'].user, total_price=0)

        total = 0
        for item in items_data:
            price = item['product'].price
            OrderItem.objects.create(order=order, price=price, **item)
            total += price * item['quantity']

        order.total_price = total
        order.save()
        return order