from django.db import models


class Paradigm(models.Model):
    """
    Describes a programming paradigm.
    """
    name = models.CharField(max_length=50)

    @property
    def number_of_languages_which_support_this_paradigm(self):
        return self.languages.count()

    @property
    def list_of_languages_which_support_this_paradigm(self):
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
    def number_of_programmers_who_know_this_language(self):
        return self.programmers.count()

    @property
    def list_of_programmers_who_know_this_language(self):
        return list(self.programmers.all())

    @property
    def number_of_frameworks(self):
        return self.frameworks.count()

    @property
    def list_of_frameworks(self):
        return list(self.frameworks.all())

    @property
    def the_most_popular_framework(self):
        number_of_programmers = 0
        popular_framework = None
        for framework in self.list_of_frameworks:
            if framework.number_of_programmers_who_knows_this_framework > number_of_programmers:
                number_of_programmers = framework.number_of_programmers_who_knows_this_framework
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
    def number_of_programmers_who_knows_this_framework(self):
        return self.programmers.count()

    @property
    def list_of_programmers_who_know_this_framework(self):
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
    languages = models.ManyToManyField(Language,
                                       related_name='programmers')
    frameworks = models.ManyToManyField(Framework,
                                        related_name='programmers')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


def the_most_popular_language():
    """
    Returns the most popular language from existing.
    """
    paradigms = Paradigm.objects.all()
    number_of_programmers = 0
    popular_language = None

    for paradigm in paradigms:
        languages = paradigm.list_of_languages_which_support_this_paradigm

        for language in languages:
            if language.number_of_programmers_who_know_this_language > number_of_programmers:
                number_of_programmers = language.number_of_programmers_who_know_this_language
                popular_language = language

    return popular_language
