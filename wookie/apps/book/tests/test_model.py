from os import remove
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.files import File
from rest_framework.test import APITestCase
from wookie.apps.book.models import Book

USER_MODEL = get_user_model()


class BookModelTests(APITestCase):
    def create_author(self):
        self.author = USER_MODEL.objects.create_user(username='David Beasley',
                                                     pseudonym='D.Beasley',
                                                     email='dbeasly@gmail.com',
                                                     password='password')

    def setUp(self):
        self.create_author()
        self.file_name = 'small.gif'
        self.file_path = 'images/book-covers/' + self.file_name
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        self.params = {
            'author': self.author,
            'title': 'Python Distilled',
            'description': 'This is a book based on my 25 years of coding',
            'price': 123354.21,
            'published': True,
            'cover_image': SimpleUploadedFile(self.file_name, small_gif, content_type='image/gif')
        }

    def test_creates_book(self):
        book = Book.objects.create(**self.params)
        self.assertIsInstance(book, Book)
        self.assertTrue(book.published)
        self.assertIs(remove(book.cover_image.path), None)

    def test_raises_error_when_no_author_is_supplied(self):
        self.params.pop('author')
        self.assertRaises(IntegrityError, Book.objects.create, **self.params)
        remove(self.file_path)

    def test_default_published_value_is_empty(self):
        self.params.pop('published')
        book = Book.objects.create(**self.params)

        self.assertIsInstance(book, Book)
        self.assertTrue(book.published)
        self.assertIs(remove(book.cover_image.path), None)

    def test_default_cover_image_value_is_empty(self):
        self.params.pop('cover_image')
        book = Book.objects.create(**self.params)

        self.assertIsInstance(book, Book)
        self.assertTrue(book.published)
        self.assertFalse(book.cover_image)
