import json
import pytest
import requests

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import Paradigm, Language, Programmer, Framework
from ..serializers import ParadigmSerializer, LanguageSerializer,\
                          ProgrammerSerializer, FrameworkSerializer


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
        self.assertEqual(response.json(), serializer.data)


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
                                    data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_single_paradigm(self):
        """
        Test case for creating the invalid paradigm.
        """
        response = self.client.post(reverse('paradigm-create'),
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

    def test_update_valid_single_paradigm(self):
        """
        Test case for a valid updating paradigm.
        """
        response = self.client.put(reverse('paradigm-update',
                                           kwargs={'pk': self.functional.pk}),
                                   data=json.dumps(self.valid_payload),
                                   content_type='application/json')
        functional_paradigm = Paradigm.objects.get(name='functional')
        serializer = ParadigmSerializer(functional_paradigm)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_update_invalid_single_paradigm(self):
        """
        Test case for an invalid updating paradigm.
        """
        response = self.client.put(reverse('paradigm-update',
                                           kwargs={'pk': self.procedure.pk}),
                                   data=json.dumps(self.invalid_payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleParadigmTest(TestCase):
    """
    Test module for deleting the existing paradigm.
    """
    def setUp(self):
        self.paradigm = Paradigm.objects.create(name='metaprogramming')

    def test_delete_valid_single_paradigm(self):
        """
        Test case for deleting the existing paradigm.
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
        Test case for getting the existing paradigm.
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
        self.assertEqual(response.json(), serializer.data)

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
                                   data=json.dumps(self.valid_payload),
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


class GetAllProgrammersTest(TestCase):
    """
    Test module for getting the list of all programmers.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        self.test_programmer1 = Programmer.objects.create(name='test_programmer1')
        self.test_programmer1.languages.add(self.test_language)
        self.test_programmer2 = Programmer.objects.create(name='test_programmer2')
        self.test_programmer2.languages.add(self.test_language)

        self.valid_list_url = reverse('programmer-list')

    def test_get_all_programmers(self):
        response = self.client.get(self.valid_list_url)
        programmers = Programmer.objects.all()
        serializer = ProgrammerSerializer(programmers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleProgrammerTest(TestCase):
    """
    Test module for getting the single programmer.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.valid_detail_url = reverse('programmer-detail',
                                        kwargs={'pk': self.test_programmer.pk})
        self.invalid_detail_url = reverse('programmer-detail',
                                          kwargs={'pk': 2000})

    def test_get_valid_single_programmer(self):
        response = self.client.get(self.valid_detail_url)
        test_programmer = Programmer.objects.get(pk=response.data['id'])
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_programmer(self):
        response = self.client.get(self.invalid_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateSingleProgrammerTest(TestCase):
    """
    Test module for creating the single programmer.
    """
    def setUp(self):
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)

        self.valid_payload = {'name': 'test_programmer',
                              'languages': [self.test_language.pk]}
        self.invalid_payload = {'name': ''}

        self.create_url = reverse('programmer-create')
        self.content_type = 'application/json'

    def test_post_valid_single_programmer(self):
        response = self.client.post(self.create_url,
                                    data=self.valid_payload,
                                    content_type=self.content_type)
        test_programmer = Programmer.objects.get(pk=response.data['id'])
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_post_invalid_single_programmer(self):
        response = self.client.post(self.create_url,
                                    data=self.invalid_payload,
                                    content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleProgrammerTest(TestCase):
    """
    Test module for updating the single programmer.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        # Create a test programmer.
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.valid_update_url = reverse('programmer-update',
                                        kwargs={'pk': self.test_programmer.pk})
        self.invalid_update_url = reverse('programmer-update',
                                          kwargs={'pk': 2000})

        self.valid_payload = {'name': 'updated_programmer',
                              'languages': [self.test_language.pk]}
        self.invalid_payload = {'name': ''}
        self.content_type = 'application/json'

    def test_update_valid_single_programmer_valid_payload(self):
        response = self.client.put(self.valid_update_url,
                                   data=json.dumps(self.valid_payload),
                                   content_type=self.content_type)
        test_programmer = Programmer.objects.get(pk=response.data['id'])
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_invalid_single_programmer_valid_payload(self):
        response = self.client.put(self.invalid_update_url,
                                   data=self.valid_payload,
                                   content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_single_programmer_invalid_payload(self):
        response = self.client.put(self.valid_update_url,
                                  data=self.invalid_payload,
                                  content_type=self.content_type)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleProgrammerTest(TestCase):
    """
    Test module for deleting the existing programmer.
    """
    def setUp(self):
        # Create a test paradigm which we will refer.
        self.test_paradigm = Paradigm.objects.create(name='test_paradigm')
        # Create a test language.
        self.test_language = Language.objects.create(name='test_language')
        self.test_language.paradigm.add(self.test_paradigm)
        # Create a test programmer.
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.valid_delete_url = reverse('programmer-delete',
                                        kwargs={'pk': self.test_programmer.pk})
        self.invalid_delete_url = reverse('programmer-delete',
                                          kwargs={'pk': 2000})

    def test_valid_delete_single_programmer(self):
        response = self.client.delete(self.valid_delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_single_programmer(self):
        response = self.client.delete(self.invalid_delete_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
