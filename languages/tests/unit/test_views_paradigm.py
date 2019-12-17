import pytest

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from languages.models import Paradigm
from languages.serializers import ParadigmSerializer


pytestmark = pytest.mark.django_db


class GetAllParadigmsTest(TestCase):
    """
    Test module for getting all paradigms.
    """
    def setUp(self):
        Paradigm.objects.create(name='procedure')
        Paradigm.objects.create(name='functional')
        Paradigm.objects.create(name='object_oriented')

    def test_get_all_paradigms(self):
        """
        Test case for getting list of existing paradigms.
        """
        # Get API response.
        response = self.client.get(reverse('paradigm-list'))
        # Get data from db.
        paradigms = Paradigm.objects.all()
        serializer = ParadigmSerializer(paradigms, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleParadigmTest(TestCase):
    """
    Test module for getting the single paradigm.
    """
    def setUp(self):
        # Create a test paradigm.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.valid_detail_url = reverse('paradigm-detail',
                                        kwargs={'pk': self.test_paradigm.pk})
        self.invalid_detail_url = reverse('paradigm-detail',
                                          kwargs={'pk': 2000})

    def test_get_valid_single_paradigm(self):
        """
        Test case for getting the existing paradigm.
        """
        # Get a paradigm instance with GET.
        response = self.client.get(self.valid_detail_url)
        # Get a paradigm instance from test db.
        test_paradigm = Paradigm.objects.get(pk=response.data['id'])
        serializer = ParadigmSerializer(test_paradigm)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_language(self):
        """
        Test case for getting the nonexistent paradigm.
        """
        # Trying to get nonexistent paradigm instance.
        response = self.client.get(self.invalid_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateSingleParadigmTest(TestCase):
    """
    Test module for creating the single paradigm.
    """
    def setUp(self):
        self.valid_payload = {'name': 'functional', }
        self.invalid_payload = {'name': '', }

    def test_create_valid_single_paradigm(self):
        """
        Test case for creating the valid paradigm.
        """
        response = self.client.post(reverse('paradigm-create'),
                                    data=self.valid_payload,
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_single_paradigm(self):
        """
        Test case for creating the invalid paradigm.
        """
        response = self.client.post(reverse('paradigm-create'),
                                    data=self.invalid_payload,
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleParadigmTest(TestCase):
    """
    Test module for updating the single paradigm.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')

        self.valid_payload = {'name': 'updated_paradigm', }
        self.invalid_payload = {'name': '', }

        self.valid_update_url = reverse('paradigm-update',
                                        kwargs={'pk': self.test_paradigm.pk})
        self.invalid_update_url = reverse('paradigm-update',
                                          kwargs={'pk': 2000})
        self.content_type = 'application/json'

    def test_update_valid_single_paradigm_valid_payload(self):
        """
        Test case for a valid updating paradigm.
        """
        response = self.client.put(self.valid_update_url,
                                   data=self.valid_payload,
                                   content_type='application/json')
        test_paradigm = Paradigm.objects.get(pk=response.data['id'])
        serializer = ParadigmSerializer(test_paradigm)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_invalid_single_paradigm_valid_payload(self):
        """
        Test case for an invalid updating paradigm.
        """
        response = self.client.put(self.invalid_update_url,
                                   data=self.valid_payload,
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_single_paradigm_invalid_payload(self):
        """
        Test case for an invalid updating paradigm.
        """
        response = self.client.put(self.valid_update_url,
                                   data=self.invalid_payload,
                                   content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleParadigmTest(TestCase):
    """
    Test module for deleting the single paradigm.
    """
    def setUp(self):
        self.paradigm = Paradigm.objects.create(name='metaprogramming')

    def test_delete_valid_single_paradigm(self):
        """
        Test case for deleting the single paradigm.
        """
        response = self.client.delete(reverse('paradigm-delete',
                                              kwargs={'pk': self.paradigm.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_single_paradigm(self):
        """
        Test case for deleting the nonexistent paradigm.
        """
        response = self.client.delete(reverse('paradigm-delete',
                                              kwargs={'pk': 1000}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
