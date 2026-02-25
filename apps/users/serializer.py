from rest_framework import serializers

from .models import User, UserProfile, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('city', 'address_line', 'is_default')

class UserProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','middle_name','birth_date','gender','email', 'addresses')

    def create(self, validated_data):
        user = self.context['request'].user
        addresses_data = validated_data.pop('addresses', [])

        profile = UserProfile.objects.create(user=user, **validated_data)

        for addr_data in addresses_data:
            address = Address.objects.create(**addr_data)
            profile.addresses.add(address)

        return profile

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if addresses_data is not None:
            instance.addresses.clear()
            for addr_data in addresses_data:
                address = Address.objects.create(**addr_data)
                instance.addresses.add(address)

        return instance