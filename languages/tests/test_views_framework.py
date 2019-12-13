import pytest

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import Paradigm, Language, Programmer, Framework
from ..serializers import ParadigmSerializer, LanguageSerializer,\
                          ProgrammerSerializer, FrameworkSerializer


pytestmark = pytest.mark.django_db


class GetAllFrameworks(TestCase):
    """
    Test module for getting all frameworks.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        # Create a test framework.
        self.test_framework1 = Framework.objects.create(name='test_framework1',
                                                        languages=self.test_language)
        self.test_framework2 = Framework.objects.create(name='test_framework2',
                                                        languages=self.test_language)
        self.test_framework3 = Framework.objects.create(name='test_framework3',
                                                        languages=self.test_language)

        self.list_url = reverse('framework-list')

    def test_get_all_frameworks(self):
        response = self.client.get(self.list_url)
        test_frameworks = Framework.objects.all()
        serializer = FrameworkSerializer(test_frameworks, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleFrameworkTest(TestCase):
    """
    Test module for getting the single framework.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        # Create a test framework.
        self.test_framework = Framework.objects.create(name='test_framework',
                                                       languages=self.test_language)

        self.valid_detail_url = reverse('framework-detail',
                                        kwargs={'pk': self.test_framework.pk})
        self.invalid_detail_url = reverse('framework-detail',
                                          kwargs={'pk': 2000})

    def test_get_valid_single_framework(self):
        response = self.client.get(self.valid_detail_url)
        test_framework = Framework.objects.get(pk=response.data['id'])
        serializer = FrameworkSerializer(test_framework)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_framework(self):
        response = self.client.get(self.invalid_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateSingleFrameworkTest(TestCase):
    """
    Test module for creating the single framework.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.valid_payload = {'name': 'test_framework',
                              'languages': self.test_language.pk}
        self.invalid_payload = {'name': ''}

        self.create_url = reverse('framework-create')
        self.content_type = 'application/json'

    def test_create_valid_single_framework(self):
        response = self.client.post(self.create_url,
                                    data=self.valid_payload,
                                    content_type=self.content_type)
        test_farmework = Framework.objects.get(pk=response.data['id'])
        serializer = FrameworkSerializer(test_farmework)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_create_invalid_single_framework(self):
        response = self.client.post(self.create_url,
                                    data=self.invalid_payload,
                                    content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleFrameworkTest(TestCase):
    """
    Test module for updating the single framework.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.test_framework = Framework.objects.create(name='test_framework',
                                                       languages=self.test_language)

        self.valid_payload = {'name': 'updated_framework',
                              'languages': self.test_language.pk}
        self.invalid_payload = {'name': ''}

        self.valid_update_url = reverse('framework-update',
                                        kwargs={'pk': self.test_framework.pk})
        self.invalid_update_url = reverse('framework-update',
                                          kwargs={'pk': 2000})
        self.content_type = 'application/json'

    def test_update_valid_single_framework_valid_payload(self):
        response = self.client.put(self.valid_update_url,
                                   data=self.valid_payload,
                                   content_type=self.content_type)
        test_framework = Framework.objects.get(pk=response.data['id'])
        serializer = FrameworkSerializer(test_framework)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_invalid_single_framework_valid_payload(self):
        response = self.client.put(self.invalid_update_url,
                                   data=self.valid_payload,
                                   content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_single_framework_invalid_payload(self):
        response = self.client.put(self.valid_update_url,
                                   data=self.invalid_payload,
                                   content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleFrameworkTest(TestCase):
    """
    Test module for deleting the single framework.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.test_framework = Framework.objects.create(name='test_framework',
                                                       languages=self.test_language)

        self.valid_delete_url = reverse('framework-delete',
                                        kwargs={'pk': self.test_framework.pk})
        self.invalid_delete_url = reverse('framework-delete',
                                          kwargs={'pk': 2000})

    def test_delete_valid_single_framework(self):
        response = self.client.delete(self.valid_delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_single_paradigm(self):
        response = self.client.delete(self.invalid_delete_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
