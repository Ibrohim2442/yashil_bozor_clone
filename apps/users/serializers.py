from rest_framework import serializers

from .models import User, UserProfile, Favorite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','middle_name','birth_date','gender','email')

class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('id', 'product', 'created_at')
        read_only_fields = ('id', 'created_at')

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs['product']

        if Favorite.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(
                {
                    'product': 'This product is already in your favorites.'
                }
            )

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Favorite.objects.create(user=user, **validated_data)