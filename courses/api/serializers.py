from rest_framework import serializers
from ..models import Subject, Module


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        modules = ModuleSerializer(many=True, read_only=True)


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['order', 'title',
                  'description',
                  ]