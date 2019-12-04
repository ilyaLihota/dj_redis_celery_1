from django.db import models


class Paradigm(models.Model):
    """
    Describes a programming paradigm.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Language(models.Model):
    """
    Describes a programming language.
    """
    name = models.CharField(max_length=50)
    paradigm = models.ForeignKey(Paradigm,
                                 related_name='languages',
                                 on_delete=models.CASCADE)

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

    def __str__(self):
        return self.name


class Programmer(models.Model):
    """
    Describes a programmer.
    """
    name = models.CharField(max_length=50)
    languages = models.ManyToManyField(Language,
                                       related_name='programmers')

    def __str__(self):
        return self.name
