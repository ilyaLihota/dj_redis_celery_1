from rest_framework import serializers

from .models import Paradigm, Language, Programmer, Framework


class ParadigmSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Paradigm
        fields = [
            'url',
            'id',
            'name',
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class LanguageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = [
            'url',
            'id',
            'name',
            'paradigm'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class ProgrammerSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Programmer
        fields = [
            'url',
            'id',
            'name',
            'likes',
            'languages'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)


class FrameworkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Framework
        fields = [
            'url',
            'id',
            'name',
            'languages'
        ]

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)
