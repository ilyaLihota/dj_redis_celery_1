import json
import requests

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, force_authenticate

from django_redis_celery.settings import ALLOWED_HOSTS
from ..models import Paradigm, Language, Programmer, Framework
from ..serializers import ParadigmSerializer, LanguageSerializer,\
                          ProgrammerSerializer, FrameworkSerializer


user = User.objects.get(username='Me')
password = 'my_password'
factory = APIRequestFactory()


class GetAllParadigmsTest(APITestCase):
    """
    Testing the list of paradigms.
    """
    def setUp(self):
        self.url = 'http://{}:8000{}'.format(ALLOWED_HOSTS[1], reverse('paradigm-list'))

    def test_paradigm_list_GET(self):
        response = requests.get(self.url,
                                auth=(user, password))
        paradigms = Paradigm.objects.all()
        print(paradigms)
        serializer = ParadigmSerializer(paradigms, many=True)
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleParadigmTest(APITestCase):
    """
    Testing GET the single paradigm.
    """
    def setUp(self):
        self.object_oriented = Paradigm.objects.create(name='object_oriented')
        self.url = reverse('paradigm-detail',
                           args=[self.object_oriented.pk],)



    def test_get_valid_single_paradigm(self):
        response = requests.get('http://{}:8000{}'.format(ALLOWED_HOSTS[1], self.url),
                                auth=(user, password))
        paradigm = Paradigm.objects.get(pk=self.object_oriented.pk)
        request = factory.get(self.url)
        serializer = ParadigmSerializer(paradigm,
                                        context={'request': request})
        self.assertEqual(response.text, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_paradigm(self):
        response = requests.get('http://{}:8000{}'.format(ALLOWED_HOSTS[1], self.url),
                                auth=(user, password))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewParadigmTest(APITestCase):
    """
    Testing POST the single paradigm.
    """
    def setUp(self):
        self.valid_payload = {'name': 'functional', }
        self.invalid_payload = {'name': '', }
        self.url = 'http://{}:8000{}'.format(ALLOWED_HOSTS[1], reverse('paradigm-create'))

    def test_create_valid_payload(self):
        response = requests.post(self.url,
                                 data=self.valid_payload,
                                 auth=(user, password))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_payload(self):
        response = requests.post(self.url,
                                 data=self.invalid_payload,
                                 auth=(user, password))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
