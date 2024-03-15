from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Account, AccountImage, AccountLink, PhysicalProduct, DigitalProduct, AccountLayout

User = get_user_model()

class AccountRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class DigitalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalProduct
        fields = ['id', 'name', 'price', 'description', 'file']


class PhysicalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalProduct
        fields = ['id', 'name', 'price', 'description', 'weight']


class AccountImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountImage
        fields = ('id', 'image', 'account')
        read_only_fields = ['id']

class AccountLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountLink
        fields = ('id', 'link')
class AccountLayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountLayout
        fields = ['id', 'account', 'page', 'layout']

class AccountSerializer(serializers.ModelSerializer):
    images = AccountImageSerializer(many=True, read_only=True)
    links = AccountLinkSerializer(many=True, read_only=True)
    layouts = AccountLayoutSerializer(many=True, read_only=True)
    products = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'email', 'firstname', 'lastname', 'username', 'description', 'about', 'images', 'links', 'products', 'layouts')
    def get_products(self, obj):
        digital_products = DigitalProductSerializer(DigitalProduct.objects.filter(account=obj), many=True).data
        physical_products = PhysicalProductSerializer(PhysicalProduct.objects.filter(account=obj), many=True).data
        return digital_products + physical_products

