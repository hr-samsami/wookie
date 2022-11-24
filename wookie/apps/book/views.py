from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.response import Response

from wookie.apps.book.filters import BookFilter
from wookie.apps.book.models import Book
from wookie.apps.book.serialisers import BookSerializer


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
