from django_filters import rest_framework as filters
from wookie.apps.book.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    author_pseudonym = filters.CharFilter(method='pseudonym_filter', label='author_pseudonym')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['title', 'description']

    def pseudonym_filter(self, queryset, name, value):
        if name == 'author_pseudonym':
            return queryset.prefetch_related('author').filter(published=True).filter(**{
                'author__pseudonym__contains': value,
            })
