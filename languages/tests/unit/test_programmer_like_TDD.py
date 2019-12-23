from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from languages.models import Language, Programmer
from languages.serializers import ProgrammerSerializer


class LikeProgrammerModelTest(TestCase):
    """
    Test module for updating the amount of programmer likes.
    """
    def setUp(self):
        self.test_language = Language.objects.create(name='test_language')
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

    def test_no_likes(self):
        self.assertEqual(self.test_programmer.likes, 0)

    def test_add_like(self):
        self.test_programmer.add_like()

        self.assertEqual(self.test_programmer.likes, 1)

    def test_remove_like(self):
        self.test_programmer.add_like()
        self.test_programmer.add_like()
        self.test_programmer.remove_like()

        self.assertEqual(self.test_programmer.likes, 1)

    def test_remove_like_if_number_likes_zero(self):
        self.test_programmer.remove_like()

        self.assertEqual(self.test_programmer.likes, 0)


class AddLikeProgrammerViewTest(TestCase):
    """
    Test module for ProgrammerAddLikeView.
    """
    def setUp(self):
        self.test_language = Language.objects.create(name='test_language')
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.add_like_url = reverse('programmer-add-like',
                                    kwargs={'pk': self.test_programmer.pk})

    def test_add_like_with_view(self):
        response = self.client.get(self.add_like_url)
        test_programmer = Programmer.objects.get(pk=response.data['id'])
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class RemoveLikeProgrammerViewTest(TestCase):
    """
    Test module for ProgrammerRemoveLikeView.
    """
    def setUp(self):
        self.test_language = Language.objects.create(name='test_language')
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.remove_like_url = reverse('programmer-remove-like',
                                       kwargs={'pk': self.test_programmer.pk})

    def test_remove_like_with_view(self):
        self.test_programmer.add_like()
        self.test_programmer.add_like()
        response = self.client.get(self.remove_like_url)
        test_programmer = Programmer.objects.get(pk=response.data['id'])
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_remove_like_if_number_likes_zero_with_view(self):
        response = self.client.get(self.remove_like_url)
        test_programmer = Programmer.objects.get(pk=response.data['id'])
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
