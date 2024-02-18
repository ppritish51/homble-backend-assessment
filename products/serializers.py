from rest_framework import serializers

from products.models import Product, Sku


class ProductListSerializer(serializers.ModelSerializer):
    """
    To show list of products.
    """

    class Meta:
        model = Product
        fields = ["name", "price"]


class SkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sku
        fields = ['product', 'size', 'selling_price', 'platform_commission', 'cost_price']


class ProductSerializer(serializers.ModelSerializer):
    skus = SkuSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'is_refrigerated', 'category', 'managed_by', 'created_at', 'edited_at', 'ingredients', 'skus']
