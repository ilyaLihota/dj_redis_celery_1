from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from languages.models import Language, Programmer
from languages.serializers import ProgrammerSerializer


class LikeProgrammerTest(TestCase):
    """
    Test module for updating the amount of programmer likes.
    """
    def setUp(self):
        self.test_language = Language.objects.create(name='test_language')
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.valid_payload = {'name': self.test_programmer.name,
                              'likes': 1,
                              'languages': [self.test_language.pk]}

        self.valid_update_url = reverse('programmer-like',
                                           kwargs={'pk': self.test_programmer.pk})

    def test_update_valid_like_programmer_valid_payload(self):
        response = self.client.put(self.valid_update_url,
                                   data=self.valid_payload,
                                   content_type='application/json')

        test_programmer = Programmer.objects.get(pk=self.test_programmer.pk)
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'], serializer.data['likes'])

    def test_update_invalid_like_programmer_valid_payload(self):
        response = self.client.put(reverse('programmer-like',
                                           kwargs={'pk': 2000}),
                                   data=self.valid_payload,
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_like_programmer_invalid_payload(self):
        response = self.client.put(self.valid_update_url,
                                   data={'name': self.test_programmer.name,
                                         'likes': 'no likes',
                                         'languages': [self.test_language.pk]},
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
