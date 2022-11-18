from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

USER_MODEL = get_user_model()


class AuthorTests(APITestCase):
    def test_creates_author(self):
        pseudonym = 'sara'
        author = USER_MODEL.objects.create_user('efaz', pseudonym=pseudonym, email='algho@gmail.com',
                                                password='password')
        self.assertIsInstance(author, USER_MODEL)
        self.assertEqual(author.pseudonym, pseudonym)
