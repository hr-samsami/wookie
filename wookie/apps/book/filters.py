from django.db.models.functions import Concat
from django_filters import rest_framework as filters, ModelChoiceFilter
from django.db.models import F, Value
from wookie.apps.author.models import Author
from wookie.apps.book.models import Book


class BookFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    author = filters.CharFilter(method='author_filter')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'description']

    def author_filter(self, queryset, name, value):
        if name == 'author':
            queryset = queryset.annotate(name=Concat(F('author__first_name'), Value(' '), F('author__last_name')))
            return queryset.filter(**{
                'name__contains': value,
            })
