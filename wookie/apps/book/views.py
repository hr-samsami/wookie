from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from wookie.apps.book.filters import BookFilter
from wookie.apps.book.models import Book
from wookie.apps.book.serialisers import BookSerializer


class BookAddView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.prefetch_related('author').all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

