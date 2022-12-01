from os import remove
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from wookie.apps.book.models import Book
from wookie.apps.book.serialisers import BookSerializer

USER_MODEL = get_user_model()


class BookViewTests(APITestCase):
    username = 'hamid'
    password = 'hamid'
    file_name = 'small.gif'
    file_path = 'images/book-covers/' + file_name
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )

    def create_author(self) -> None:
        self.author = USER_MODEL.objects.create_user(username=self.username,
                                                     pseudonym='h.samsami',
                                                     email='hamidreza.samsami@gmail.com',
                                                     password=self.password)

    def get_token(self) -> None:
        resp = self.client.post(reverse('token_obtain_pair'),
                                data={'username': self.username, 'password': self.password})
        self.token = f'Bearer {resp.data["access"]}'


# Test for path('create/', views.book_create, name='book-create')
class CreateBookViewTests(BookViewTests):
    def setUp(self):
        self.create_author()
        self.get_token()
        self.params = {
            'title': 'Python Distilled',
            'description': 'This is a book based on my 25 years of coding',
            'price': 123354.21,
            'published': True,
            'cover_image': SimpleUploadedFile(self.file_name, self.small_gif, content_type='image/gif')
        }

    def test_response_401_if_user_not_login(self):
        resp = self.client.post(reverse('book-create'), data=self.params)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', resp.json()['detail'])
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_create_book(self):
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        book = Book.objects.get(id=resp.json()['id'])
        serializer = BookSerializer(book)

        self.assertIsNone(remove(book.cover_image.path))
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_title_miss(self):
        self.params.pop('title')
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        self.assertEqual(resp.json()['title'][0], 'This field is required.')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_title_empty(self):
        self.params['title'] = ''
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        self.assertEqual(resp.json()['title'][0], 'This field may not be blank.')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_description_miss(self):
        self.params.pop('description')
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        self.assertEqual(resp.json()['description'][0], 'This field is required.')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_description_empty(self):
        self.params['description'] = ''
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        self.assertEqual(resp.json()['description'][0], 'This field may not be blank.')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_when_cover_image_miss(self):
        self.params.pop('cover_image')
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        book = Book.objects.get(id=resp.json()['id'])
        serializer = BookSerializer(book)

        self.assertFalse(bool(book.cover_image))
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_price_miss(self):
        self.params.pop('price')
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        self.assertEqual(resp.json()['price'][0], 'This field is required.')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_price_more_than_then_digits(self):
        self.params['price'] = 12345678912.32
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        self.assertIn('digits in total.', resp.json()['price'][0])
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_default_false_when_published_miss(self):
        self.params.pop('published')
        resp = self.client.post(reverse('book-create'), HTTP_AUTHORIZATION=self.token, data=self.params)
        book = Book.objects.get(id=resp.json()['id'])
        serializer = BookSerializer(book)
        self.assertFalse(book.published)
        self.assertIsNone(remove(book.cover_image.path))
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue('application/json' in resp['Content-Type'])
