from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse


class Paradigm(models.Model):
    """
    Describes a programming paradigm.
    """
    name = models.CharField(max_length=50)

    @property
    def number_languages_support_paradigm(self):
        return self.languages.count()

    @property
    def list_languages_support_paradigm(self):
        return list(self.languages.all())

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Describes a programming language.
    """
    name = models.CharField(max_length=50)
    paradigm = models.ManyToManyField(Paradigm,
                                      related_name='languages')

    @property
    def number_programmers_know_language(self):
        return self.programmers.count()

    @property
    def list_programmers_know_language(self):
        return list(self.programmers.all())

    @property
    def number_frameworks(self):
        return self.frameworks.count()

    @property
    def list_frameworks(self):
        return list(self.frameworks.all())

    @property
    def most_popular_framework(self):
        number_programmers = 0
        popular_framework = None
        for framework in self.list_frameworks:
            if framework.number_programmers_know_framework > number_programmers:
                number_programmers = framework.number_programmers_know_framework
                popular_framework = framework
        return popular_framework

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Framework(models.Model):
    """
    Describes a framework.
    """
    name = models.CharField(max_length=50)
    languages = models.ForeignKey(Language,
                                  related_name='frameworks',
                                  on_delete=models.CASCADE)

    @property
    def number_programmers_know_framework(self):
        return self.programmers.count()

    @property
    def list_programmers_know_framework(self):
        return list(self.programmers.all())

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Programmer(models.Model):
    """
    Describes a programmer.
    """
    name = models.CharField(max_length=50)
    likes = models.PositiveIntegerField(default=0)
    languages = models.ManyToManyField(Language,
                                       related_name='programmers')
    frameworks = models.ManyToManyField(Framework,
                                        related_name='programmers')

    @property
    def number_likes(self):
        return self.likes

    def add_like(self, user):
        if self not in user.liked_programmers.all():
            self.likes += 1
            self.users_like.add(user)
            self.save()

    def remove_like(self, user):
        if self in user.liked_programmers.all() and self.likes > 0:
            self.users_like.remove(user)
            self.likes -= 1
            self.save()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


def most_popular_language():
    """
    Returns the most popular language from existing.
    """
    languages = Language.objects.all()
    number_programmers = 0
    popular_language = None

    for language in languages:
        if language.number_programmers_know_language > number_programmers:
            number_programmers = language.number_programmers_know_language
            popular_language = language

    return popular_language


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked_programmers = models.ManyToManyField(Programmer,
                                               related_name='users_like')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
