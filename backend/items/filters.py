import django_filters
from .models import Item, Category

class ItemFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    location = django_filters.CharFilter(lookup_expr='icontains')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    condition = django_filters.ChoiceFilter(choices=Item.CONDITION_CHOICES)
    price_type = django_filters.ChoiceFilter(choices=Item.PRICE_TYPE_CHOICES)

    class Meta:
        model = Item
        fields = ['category', 'location', 'condition', 'price_type']
