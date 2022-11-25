from rest_framework import serializers
from wookie.apps.book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author_name', 'cover_image', 'price']
        extra_kwargs = {
            'author_name': {'read_only': True}
        }
