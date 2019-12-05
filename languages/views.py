from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Paradigm, Language, Programmer, Framework
from .serializers import ParadigmSerializer, LanguageSerializer, ProgrammerSerializer, FrameworkSerializer


class ParadigmListView(APIView):
    """
    Retrieve a list of paradigms or create a paradigm instance.
    """
    def get(self, request):
        paradigms = Paradigm.objects.all()
        serializer = ParadigmSerializer(paradigms, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = ParadigmSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParadigmDetailView(APIView):
    """
    Retrieve, update or delete a paradigm instance.
    """
    def get_object(self, pk):
        try:
            return Paradigm.objects.get(pk=pk)
        except Paradigm.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        paradigm = self.get_object(pk)
        serializer = ParadigmSerializer(paradigm)
        return Response(serializer.data)

    def put(self, request, pk):
        paradigm = self.get_object(pk)
        serializer = ParadigmSerializer(paradigm, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        paradigm = self.get_object(pk)
        paradigm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class LanguageListView(APIView):
    """
    Retrieve a list of languages or create a language instance.
    """
    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = LanguageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageDetailView(APIView):
    """
    Retrieve, update or delete a language instance.
    """
    def get_object(self, pk):
        try:
            return Language.objects.get(pk=pk)
        except Language.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        language = self.get_object(pk)
        serializer = LanguageSerializer(language)
        return Response(serializer.data)

    def put(self, request, pk):
        language = self.get_object(pk)
        serializer = LanguageSerializer(language, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        language = self.get_object(pk)
        language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProgrammerListView(APIView):
    """
    Retrieve a list of programmers or create a programmer instance.
    """
    def get(self, request):
        programmers = Programmer.objects.all()
        serializer = ProgrammerSerializer(programmers, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = ProgrammerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgrammerDetailView(APIView):
    """
    Retrieve, update or delete a programmer instance.
    """
    def get_object(self, pk):
        try:
            return Programmer.objects.get(pk=pk)
        except Programmer.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        programmer = self.get_object(pk)
        serializer = ProgrammerSerializer(programmer)
        return Response(serializer.data)

    def put(self, request, pk):
        programmer = self.get_object(pk)
        serializer = ProgrammerSerializer(programmer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, sttaus=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        programmer = self.get_object(pk)
        programmer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FrameworkListView(APIView):
    """
    Retrieve a list of frameworks or create a framework instance.
    """
    def get(self, request):
        frameworks = Framework.objects.all()
        serializer = FrameworkSerializer(frameworks, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = FrameworkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FrameworkDetailView(APIView):
    """
    Retrieve, update or delete a framework instance.
    """
    def get_object(self, pk):
        try:
            return Framework.objects.get(pk=pk)
        except Framework.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        framework = self.get_object(pk)
        serializer = FrameworkSerializer(framework)
        return Response(serializer.data)

    def put(self, request, pk):
        framework = self.get_object(pk)
        serializer = FrameworkSerializer(framework, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        framework = self.get_object(pk)
        framework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
