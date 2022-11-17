from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RendererTests(APITestCase):
    def setUp(self):
        self.json_type = 'application/json'
        self.xml_type = 'application/xml'
        self.url = reverse('renderer')

    def test_response_default_content_type_is_json(self):
        """
        Ensure default Content-Type for non XML type is JSON.
        """
        sample_types = ['text/css', 'image/gif', 'text/html']
        for ct in sample_types:
            resp = self.client.get(self.url, content_type=ct)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            self.assertTrue('application/json' in resp['Content-Type'])

    def test_json_response_when_content_type_is_json(self):
        """
        Ensure when Content-Type in the header request is application/json then the response is JSON too.
        """
        resp = self.client.get(self.url, content_type=self.json_type)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(self.json_type in resp['Content-Type'])

    def test_xml_response_when_content_type_is_xml(self):
        """
        Ensure when Content-Type in the header request is application/xml then the response is XML too.
        """
        resp = self.client.get(self.url, content_type=self.xml_type)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(self.xml_type in resp['Content-Type'])
