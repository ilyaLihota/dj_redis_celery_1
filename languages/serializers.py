from rest_framework import serializers

from .models import Paradigm, Language, Programmer, Framework


class ParadigmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Paradigm
        fields = ['url', 'id', 'name']


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ['url', 'id', 'name', 'paradigm']


class ProgrammerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Programmer
        fields = ['url', 'id', 'name', 'languages']


class FrameworkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Framework
        fields = ['url', 'id', 'name', 'languages']
