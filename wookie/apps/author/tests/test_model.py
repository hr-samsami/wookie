from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

USER_MODEL = get_user_model()


class AuthorTests(APITestCase):
    def setUp(self):
        self.username = 'efaz'
        self.email = 'algho@gmail.com'
        self.pseudonym = 'sara'
        self.password = 'password'

    def test_creates_author(self):
        author = USER_MODEL.objects.create_user(username=self.username,
                                                pseudonym=self.pseudonym,
                                                email=self.email,
                                                password=self.password)
        self.assertIsInstance(author, USER_MODEL)
        self.assertFalse(author.is_staff)
        self.assertEqual(author.pseudonym, self.pseudonym)

    def test_creates_super_user(self):
        author = USER_MODEL.objects.create_superuser(username=self.username,
                                                     pseudonym=self.pseudonym,
                                                     email=self.email,
                                                     password=self.password)
        self.assertIsInstance(author, USER_MODEL)
        self.assertTrue(author.is_staff)
        self.assertEqual(author.pseudonym, self.pseudonym)

    def test_raises_error_when_no_username_is_supplied(self):
        self.assertRaises(TypeError, USER_MODEL.objects.create_user,
                          pseudonym=self.pseudonym,
                          email=self.email,
                          password=self.password)

    def test_default_pseudonym_value_is_empty(self):
        author = USER_MODEL.objects.create_user(username=self.username,
                                                email=self.email,
                                                password=self.password)
        self.assertIsInstance(author, USER_MODEL)
        self.assertFalse(author.is_staff)
        self.assertEqual(author.pseudonym, None)
