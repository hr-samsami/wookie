from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_books(request):
    books = Book.objects.prefetch_related('author').filter(author=request.user).all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    book = Book.objects.prefetch_related('author').filter(author=request.user).filter(id=pk).first()
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_create(request):
    serializer = BookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_update(request, pk):
    book = Book.objects.prefetch_related('author').filter(author=request.user).filter(id=pk).first()
    serializer = BookSerializer(instance=book, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_delete(request, pk):
    book = Book.objects.prefetch_related('author').filter(author=request.user).filter(id=pk).get()
    book.delete()
    return Response('Deleted', status=status.HTTP_200_OK)



