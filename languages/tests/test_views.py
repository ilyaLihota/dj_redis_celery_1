import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase,\
                                APIRequestFactory, force_authenticate,\
                                RequestsClient

from ..models import Paradigm, Language, Programmer, Framework
from ..serializers import ParadigmSerializer, LanguageSerializer,\
                          ProgrammerSerializer, FrameworkSerializer


client = Client()
factory = APIRequestFactory()


class GetAllParadigmsTest(TestCase):
    """
    Test module for GET all paradigms API.
    """
    def setUp(self):
        Paradigm.objects.create(name='procedure')

    def test_get_all_paradigms(self):
        # Get API response.
        response = client.get(reverse('paradigm-list'))
        # Get data from db.
        paradigms = Paradigm.objects.all()
        serializer = ParadigmSerializer(paradigms, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)


class GetSingleParadigmTest(TestCase):
    """
    Test module for getting the existing paradigm.
    """
    def setUp(self):
        self.paradigm = Paradigm.objects.create(name='my_paradigm')

    def test_get_valid_single_paradigm(self):
        response = client.get(reverse('paradigm-detail',
                                      args=[self.paradigm.pk]))
        paradigm = Paradigm.objects.get(name='my_paradigm')
        serializer = ParadigmSerializer(paradigm)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_get_invalid_single_paradigm(self):
        response = client.get(reverse('paradigm-detail', args=[100, ]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewParadigmTest(TestCase):
    """
    Test module for inserting a new paradigm.
    """
    def setUp(self):
        self.valid_payload = {'name': 'functional', }
        self.invalid_payload = {'name': '', }

    def test_create_valid_paradigm(self):
        response = client.post(reverse('paradigm-create'),
                               data=json.dumps(self.valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_paradigm(self):
        response = client.post(reverse('paradigm-create'),
                               data=json.dumps(self.invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleParadigmTest(TestCase):
    """
    Test module for updating the existing paradigm.
    """
    def setUp(self):
        self.functional = Paradigm.objects.create(name='functional')
        self.procedure = Paradigm.objects.create(name='procedure')
        self.valid_payload = {'name': 'functional', }
        self.invalid_payload = {'name': '', }

    def test_valid_update_paradigm(self):
        response = client.put(reverse('paradigm-update', args=[self.functional.pk]),
                              data=json.dumps(self.valid_payload),
                              content_type='application/json')
        functional_paradigm = Paradigm.objects.get(name='functional')
        serializer = ParadigmSerializer(functional_paradigm)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_invalid_update_paradigm(self):
        response = client.put(reverse('paradigm-update', args=[self.procedure.pk]),
                              data=json.dumps(self.invalid_payload),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleParadigmTest(TestCase):
    """
    Test module for deleting the existing paradigm.
    """
    def setUp(self):
        self.paradigm = Paradigm.objects.create(name='metaprogramming')

    def test_valid_delete_single_paradigm(self):
        response = client.delete(reverse('paradigm-delete', args=[self.paradigm.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_single_paradigm(self):
        response = client.delete(reverse('paradigm-delete', args=[1000, ]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
