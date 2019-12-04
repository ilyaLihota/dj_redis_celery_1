from rest_framework import serializers
from .models import Paradigm, Language, Programmer, Framework


class ParadigmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paradigm
        fields = ['id', 'url', 'name']


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'url', 'name', 'paradigm']


class ProgrammersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Programmer
        fields = ['id', 'url', 'name', 'languages']


class FrameworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Framework
        fields = ['id', 'url', 'name', 'languages']