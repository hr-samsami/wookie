from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, parsers
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from wookie.apps.book.filters import BookFilter
from wookie.apps.book.models import Book
from wookie.apps.book.serialisers import BookSerializer


class BookView(APIView):
    queryset = Book.objects.none()
    permission_classes = (DjangoModelPermissions,)

    def get(self, request, id=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({'data': serializer.data})

    @swagger_auto_schema(request_body=BookSerializer)
    def post(self, request, id=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.prefetch_related('author').filter(published=True).all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter
    permission_classes = (AllowAny,)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_books(request):
    books = list(Book.objects.prefetch_related('author').filter(author=request.user).all())
    if len(books) > 0:
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response('Book Not Found', status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    try:
        book = Book.objects.prefetch_related('author').filter(author=request.user).get(id=pk)
    except Book.DoesNotExist:
        return Response('Book Not Found', status=status.HTTP_404_NOT_FOUND)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=BookSerializer)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([parsers.MultiPartParser, parsers.FormParser])
def book_create(request):
    serializer = BookSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='put', request_body=BookSerializer)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([parsers.MultiPartParser, parsers.FormParser])
def book_update(request, pk):
    try:
        book = Book.objects.prefetch_related('author').filter(author=request.user).get(id=pk)
    except Book.DoesNotExist:
        return Response('Book Not Found', status=status.HTTP_404_NOT_FOUND)
    serializer = BookSerializer(instance=book, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_unpublish(request, pk):
    updated = Book.objects.prefetch_related('author')\
        .filter(author=request.user)\
        .filter(id=pk)\
        .update(published=False)
    if updated:
        return Response('Book Unpublished', status=status.HTTP_200_OK)
    else:
        return Response('Book Not Found', status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_delete(request, pk):
    try:
        book = Book.objects.prefetch_related('author').filter(author=request.user).filter(id=pk).get()
    except Book.DoesNotExist:
        return Response('Book Not Found', status=status.HTTP_404_NOT_FOUND)
    book.delete()
    return Response('Book Deleted', status=status.HTTP_200_OK)
