from rest_framework import serializers

from .models import Paradigm, Language, Programmer, Framework


class ParadigmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paradigm
        fields = [
            'id',
            'name',
        ]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = [
            'id',
            'name',
            'paradigm'
        ]


class ProgrammerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programmer
        fields = [
            'id',
            'name',
            'likes',
            'languages'
        ]


class FrameworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Framework
        fields = [
            'id',
            'name',
            'languages'
        ]
