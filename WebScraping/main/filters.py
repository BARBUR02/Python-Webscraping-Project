import django_filters
from .models import Offert

SUBJECTS = [
        ("Język polski", "Język polski"),
        ("Język angielski", "Język angielski"),
        ("Matematyka", "Matematyka"),
        ("Fizyka", "Fizyka"),
        ("Chemia", "Chemia"),
    ]

class OfferFilter(django_filters.FilterSet):
    subject = django_filters.ChoiceFilter(
        choices=SUBJECTS,
        label="Przedmiot",
        )
    minPrice = django_filters.RangeFilter(
        
        label="Cena"
        )
    locations = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Miejscowość"
        )
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label="Nazwa"
        )
    class Meta:
        model = Offert
        fields = ['subject', 'minPrice', 'locations', 'name']