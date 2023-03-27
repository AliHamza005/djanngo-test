from rest_framework import serializers
from decimal import Decimal
from store.models import Product,Collection

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']

    products_count = serializers.IntegerField(read_only = True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','unit_price','inventory','price_with_tax','collection']

    price_with_tax = serializers.SerializerMethodField('calculate_tax')
    #collection = CollectionSerializer()

    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
        