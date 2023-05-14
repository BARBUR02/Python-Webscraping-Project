import django_filters
from .models import Offert


class OfferFilter(django_filters.FilterSet):
    minPrice = django_filters.RangeFilter()
    class Meta:
        model = Offert
        fields = {
            'name': ['icontains'],
            'subject': ['exact'] ,
            # 'minPrice': ['lt'],
            'locations': ['icontains'],
        }