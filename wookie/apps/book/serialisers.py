from rest_framework import serializers
from wookie.apps.book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_pseudonym', 'description', 'cover_image', 'price', 'published']
        extra_kwargs = {
            'author_pseudonym': {'read_only': True}

        }
