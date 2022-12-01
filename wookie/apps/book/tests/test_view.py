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


# Test for path('update/<int:pk>/', views.book_update, name='book-update')
class UpdateBookViewTests(BookViewTests):
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
        self.book = Book.objects.create(author=self.author, **self.params)
        remove(self.book.cover_image.path)
        self.url = reverse('book-update', kwargs={'pk': self.book.id})

    def test_response_401_if_user_not_login(self):
        resp = self.client.post(self.url, data=self.params)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', resp.json()['detail'])
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_update_book(self):
        self.params = {
            'title': 'Python-2022',
            'description': 'This is a book based on my 30 years of coding',
            'price': 1200,
            'published': False,
            'cover_image': SimpleUploadedFile(self.file_name, self.small_gif, content_type='image/gif')
        }
        resp = self.client.put(self.url, HTTP_AUTHORIZATION=self.token, data=self.params)
        book = Book.objects.get(id=resp.json()['id'])
        serializer = BookSerializer(book)

        self.assertIsNone(remove(book.cover_image.path))
        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_author_is_not_owner(self):
        USER_MODEL.objects.create_user(username='reza',
                                       pseudonym='f.reza',
                                       email='reza@gmail.com',
                                       password=self.password)

        resp = self.client.post(reverse('token_obtain_pair'), data={'username': 'reza', 'password': self.password})
        self.token = f'Bearer {resp.data["access"]}'
        resp = self.client.put(self.url, HTTP_AUTHORIZATION=self.token, data=self.params)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('application/json' in resp['Content-Type'])


# Test for path('delete/<int:pk>/', views.book_delete, name='book-delete')
class DeleteBookViewTests(BookViewTests):
    def setUp(self):
        self.create_author()
        self.get_token()
        self.params = {
            'title': 'Python Distilled 2022',
            'description': 'This is a book based on my 25 years of coding',
            'price': 123354.21,
            'published': True,
            'cover_image': SimpleUploadedFile(self.file_name, self.small_gif, content_type='image/gif')
        }
        self.book = Book.objects.create(author=self.author, **self.params)
        remove(self.book.cover_image.path)
        self.url = reverse('book-delete', kwargs={'pk': self.book.id})

    def test_response_401_if_user_not_login(self):
        resp = self.client.delete(self.url, data=self.params)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', resp.json()['detail'])
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_delete_book(self):
        resp = self.client.delete(self.url, HTTP_AUTHORIZATION=self.token)
        book = Book.objects.filter(id=self.book.id).first()

        self.assertIsNone(book)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('application/json' in resp['Content-Type'])

        resp = self.client.delete(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_author_is_not_owner(self):
        USER_MODEL.objects.create_user(username='reza',
                                       pseudonym='f.reza',
                                       email='reza@gmail.com',
                                       password=self.password)

        resp = self.client.post(reverse('token_obtain_pair'), data={'username': 'reza', 'password': self.password})
        self.token = f'Bearer {resp.data["access"]}'
        resp = self.client.delete(self.url, HTTP_AUTHORIZATION=self.token, data=self.params)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('application/json' in resp['Content-Type'])


# Test for path('unpublish/<int:pk>/', views.book_unpublish, name='book-unpublish')
class UnpublishBookViewTests(BookViewTests):
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
        self.book = Book.objects.create(author=self.author, **self.params)
        self.assertTrue(self.book.published)
        remove(self.book.cover_image.path)
        self.url = reverse('book-unpublish', kwargs={'pk': self.book.id})

    def test_response_401_if_user_not_login(self):
        resp = self.client.patch(self.url, data=self.params)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', resp.json()['detail'])
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_unpublished_book(self):
        resp = self.client.patch(self.url, HTTP_AUTHORIZATION=self.token)
        book = Book.objects.get(id=self.book.id)

        self.assertFalse(book.published)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_author_is_not_owner(self):
        USER_MODEL.objects.create_user(username='reza',
                                       pseudonym='f.reza',
                                       email='reza@gmail.com',
                                       password=self.password)

        resp = self.client.post(reverse('token_obtain_pair'), data={'username': 'reza', 'password': self.password})
        self.token = f'Bearer {resp.data["access"]}'
        resp = self.client.patch(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('application/json' in resp['Content-Type'])


# Test for path('detail/<int:pk>/', views.book_detail, name='book-detail'),
class DetailBookViewTests(BookViewTests):
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
        self.book = Book.objects.create(author=self.author, **self.params)
        remove(self.book.cover_image.path)
        self.url = reverse('book-detail', kwargs={'pk': self.book.id})

    def test_response_401_if_user_not_login(self):
        resp = self.client.get(self.url, data=self.params)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials were not provided.', resp.json()['detail'])
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_detail_book(self):
        resp = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        book = Book.objects.get(id=self.book.id)
        serializer = BookSerializer(book)

        self.assertEqual(resp.data, serializer.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('application/json' in resp['Content-Type'])

    def test_response_raise_when_author_is_not_owner(self):
        USER_MODEL.objects.create_user(username='reza',
                                       pseudonym='f.reza',
                                       email='reza@gmail.com',
                                       password=self.password)

        resp = self.client.post(reverse('token_obtain_pair'), data={'username': 'reza', 'password': self.password})
        self.token = f'Bearer {resp.data["access"]}'
        resp = self.client.get(self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue('application/json' in resp['Content-Type'])
