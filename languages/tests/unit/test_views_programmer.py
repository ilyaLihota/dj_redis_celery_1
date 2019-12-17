import pytest

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from languages.models import Paradigm, Language, Programmer
from languages.serializers import ProgrammerSerializer


pytestmark = pytest.mark.django_db


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

        self.list_url = reverse('programmer-list')

    def test_get_all_programmers(self):
        response = self.client.get(self.list_url)
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
                                   data=self.valid_payload,
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
    Test module for deleting the single programmer.
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

    def test_delete_valid_single_programmer(self):
        response = self.client.delete(self.valid_delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_single_programmer(self):
        response = self.client.delete(self.invalid_delete_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)