import pytest

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import Paradigm, Language, Programmer, Framework
from ..serializers import ParadigmSerializer, LanguageSerializer,\
                          ProgrammerSerializer, FrameworkSerializer


pytestmark = pytest.mark.django_db


class GetAllLanguagesTest(TestCase):
    """
    Test module for getting all languages.
    """
    def setUp(self):
        self.test_paradigm1 = Paradigm.objects.create(name='functional')
        self.test_paradigm2 = Paradigm.objects.create(name='procedure')
        self.test_paradigm3 = Paradigm.objects.create(name='object_oriented')

        self.test_language1 = Language.objects.create(name='Scala')
        self.test_language1.paradigm.set([self.test_paradigm1])
        self.test_language2 = Language.objects.create(name='Python')
        self.test_language2.paradigm.set([self.test_paradigm2])
        self.test_language3 = Language.objects.create(name='Java')
        self.test_language3.paradigm.set([self.test_paradigm3])

        self.list_url = reverse('language-list')

    def test_get_all_paradigms(self):
        """
        Test case for getting list of existing languages.
        """
        # Get API response.
        response = self.client.get(self.list_url)
        # Get data from db.
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleLanguageTest(TestCase):
    """
    Test module for getting the single paradigm.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.valid_detail_url = reverse('language-detail',
                                  kwargs={'pk': self.test_language.pk})
        self.invalid_detail_url = reverse('language-detail',
                                          kwargs={'pk': 2000})

    def test_get_valid_single_language(self):
        """
        Test case for getting the single paradigm.
        """
        # Get a language instance with GET.
        response = self.client.get(self.valid_detail_url)
        # Get a language instance from test db.
        test_language = Language.objects.get(pk=response.data['id'])
        serializer = LanguageSerializer(test_language)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_language(self):
        """
        Test case for getting the nonexistent paradigm.
        """
        # Trying to get nonexistent language instance.
        response = self.client.get(self.invalid_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateSingleLanguageTest(TestCase):
    """
    Test module for creating the single language instance.
    """
    def setUp(self):
        self.create_url = reverse('language-create')
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')

    def test_post_valid_single_language(self):
        """
        Test case for creating a valid language instance.
        """
        # Create a language instance with POST.
        response = self.client.post(self.create_url,
                                    data={'name': 'test_language',
                                          'paradigm': [self.test_paradigm.pk]},
                                    content_type='application/json')
        # Get created language instance from test db.
        test_language = Language.objects.get(pk=response.data['id'])
        serializer = LanguageSerializer(test_language)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_post_invalid_single_language(self):
        """
        Test case for creating language with the nonexistent paradigm.
        """
        # Trying to create an invalid language instance with POST.
        response = self.client.post(self.create_url,
                                    data={'name': 'test_invalid_language',
                                          'paradigm': [2000, ]},
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleLanguageTest(TestCase):
    """
    Test module for updating the single language instance.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.valid_update_url = reverse('language-update',
                                        kwargs={'pk': self.test_language.pk})
        self.invalid_update_url = reverse('language-update',
                                          kwargs={'pk': 2000})

        self.valid_payload = {'name': 'updated_language',
                              'paradigm': [self.test_paradigm.pk]}
        self.invalid_payload = {'name': ''}
        self.content_type = 'application/json'

    def test_update_valid_single_language_valid_payload(self):
        response = self.client.put(self.valid_update_url,
                                   data=self.valid_payload,
                                   content_type=self.content_type)
        test_language = Language.objects.get(pk=self.test_language.pk)
        serializer = LanguageSerializer(test_language)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_invalid_single_language_valid_payload(self):
        response = self.client.put(self.invalid_update_url,
                                   data=self.valid_payload,
                                   content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_single_language_invalid_payload(self):
        response = self.client.put(self.valid_update_url,
                                   data=self.invalid_payload,
                                   content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleLanguageTest(TestCase):
    """
    Test module for deleting the single language instance.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.valid_delete_url = reverse('language-delete',
                                        kwargs={'pk': self.test_language.pk})
        self.invalid_delete_url = reverse('language-delete',
                                          kwargs={'pk': 2000})

    def test_delete_valid_single_language(self):
        response = self.client.delete(self.valid_delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_single_language(self):
        response = self.client.delete(self.invalid_delete_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)