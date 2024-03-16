from rest_framework import serializers

from accounts.serializers import AccountImageSerializer
from .models import Layout, LayoutHeader, LayoutBody, LayoutFooter, LayoutComponent, LayoutText, LayoutSetting


class LayoutTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayoutText
        fields = '__all__'


class LayoutSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayoutSetting
        fields = '__all__'


class LayoutComponentSerializer(serializers.ModelSerializer):
    images = AccountImageSerializer(many=True, read_only=True)
    settings = LayoutSettingSerializer(many=True)
    texts = LayoutTextSerializer(many=True)
    class Meta:
        model = LayoutComponent
        fields = '__all__'


class LayoutHeaderSerializer(serializers.ModelSerializer):
    components = LayoutComponentSerializer(many=True, read_only=True)

    class Meta:
        model = LayoutHeader
        fields = '__all__'


class LayoutBodySerializer(serializers.ModelSerializer):
    components = LayoutComponentSerializer(many=True, read_only=True)

    class Meta:
        model = LayoutBody
        fields = '__all__'


class LayoutFooterSerializer(serializers.ModelSerializer):
    components = LayoutComponentSerializer(many=True, read_only=True)

    class Meta:
        model = LayoutFooter
        fields = '__all__'




class LayoutSerializer(serializers.ModelSerializer):
    headers = LayoutHeaderSerializer(many=True)
    bodies = LayoutBodySerializer(many=True)
    footers = LayoutFooterSerializer(many=True)
    class Meta:
        model = Layout
        fields = '__all__'
