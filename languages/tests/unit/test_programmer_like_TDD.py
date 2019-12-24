from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from languages.models import Language, Programmer, Profile
from languages.serializers import ProgrammerSerializer


class ProfileModelTest(APITestCase):
    """
    Test module for checking Profile model.
    """
    def setUp(self):
        self.user = User.objects.create(username='test_user',
                                        password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_profile_item(self):
        profiles = Profile.objects.all()

        self.assertEqual(profiles.count(), 1)


class LikeProgrammerModelTest(APITestCase):
    """
    Test module for updating the amount of programmer likes.
    """
    def setUp(self):
        self.user = User.objects.create(username='test_user',
                                        password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.test_language = Language.objects.create(name='test_language')
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

    def test_no_likes(self):
        self.assertEqual(self.test_programmer.likes, 0)

    def test_add_like(self):
        self.test_programmer.add_like(self.user.profile)

        self.assertEqual(self.test_programmer.likes, 1)

    def test_remove_like(self):
        self.test_programmer.add_like(self.user.profile)
        self.test_programmer.remove_like(self.user.profile)

        self.assertEqual(self.test_programmer.likes, 0)

    def test_remove_like_if_number_likes_zero(self):
        self.test_programmer.remove_like(self.user.profile)

        self.assertEqual(self.test_programmer.likes, 0)


class NumberProgrammerLikesViewTest(APITestCase):
    """
    Test module for ProgrammerLikesView.
    """
    def setUp(self):
        self.user = User.objects.create(username='test_user',
                                        password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.test_language = Language.objects.create(name='test_language')
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

    def test_get_number_likes_with_view(self):
        response = self.client.get(reverse('programmer-likes',
                                           kwargs={'pk': self.test_programmer.pk}))
        test_programmer = Programmer.objects.get(pk=self.test_programmer.pk)
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data['likes'])


class AddLikeProgrammerViewTest(APITestCase):
    """
    Test module for ProgrammerAddLikeView.
    """
    def setUp(self):
        self.user = User.objects.create(username='test_user',
                                        password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.test_language = Language.objects.create(name='test_language')
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.add_like_url = reverse('programmer-add-like',
                                    kwargs={'pk': self.test_programmer.pk})

    def test_add_like_with_view(self):
        response = self.client.patch(self.add_like_url)
        test_programmer = Programmer.objects.get(pk=self.test_programmer.pk)
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class RemoveLikeProgrammerViewTest(APITestCase):
    """
    Test module for ProgrammerRemoveLikeView.
    """
    def setUp(self):
        self.user = User.objects.create(username='test_user',
                                        password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.test_language = Language.objects.create(name='test_language')
        self.test_programmer = Programmer.objects.create(name='test_programmer')
        self.test_programmer.languages.add(self.test_language)

        self.remove_like_url = reverse('programmer-remove-like',
                                       kwargs={'pk': self.test_programmer.pk})

    def test_remove_like_with_view(self):
        self.test_programmer.add_like(self.user.profile)
        self.test_programmer.add_like(self.user.profile)
        response = self.client.patch(self.remove_like_url)
        test_programmer = Programmer.objects.get(pk=self.test_programmer.pk)
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_remove_like_if_number_likes_zero_with_view(self):
        response = self.client.patch(self.remove_like_url)
        test_programmer = Programmer.objects.get(pk=self.test_programmer.pk)
        serializer = ProgrammerSerializer(test_programmer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
