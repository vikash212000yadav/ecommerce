from django.db.models import Max, Min
from rest_framework import serializers

from product.models import Product
from tag.serializers import TagSerializer


class ProductListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True, source='tag-set')
    prices = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'tags', 'prices', 'image')

    def get_prices(self, obj):
        prices = obj.unit_set.aggregate(max=Max('price'), min=Min('price'))
        return {
            'min': prices['min'],
            'max': prices['max']
        }

    def get_image(self, obj):
        unit = obj.unit_set.filter(unitimage_isnull=False).first()
        if unit is None:
            return None

        image = unit.unitimage_set.order_by('-is_main').first()
        if image is None:
            return None

        return image.image.url


#class ProductSerializer(ProductListSerializer):