from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, renderers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Paradigm, Language, Programmer, Framework
from .serializers import ParadigmSerializer, LanguageSerializer, ProgrammerSerializer, FrameworkSerializer


@api_view(['GET'])
def api_root(request, format=None):
    """
    The entry point to API.
    """
    return Response({
        'paradigms': reverse('paradigm-list', request=request, format=format),
        'languages': reverse('language-list', request=request, format=format),
        'programmers': reverse('programmer-list', request=request, format=format),
        'frameworks': reverse('framework-list', request=request, format=format),
    })


class ParadigmListView(APIView):
    """
    Retrieve a list of paradigms.
    """
    def get(self, request):
        paradigms = Paradigm.objects.all()
        serializer = ParadigmSerializer(paradigms,
                                        many=True,
                                        context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class ParadigmCreateView(APIView):
    """
    Create the paradigm instance.
    """
    def post(self, request):
        data = request.data
        serializer = ParadigmSerializer(data=data,
                                        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParadigmDetailView(APIView):
    """
    Retrieve the paradigm instance.
    """
    def get(self, request, pk):
        paradigm = get_object_or_404(Paradigm, pk=pk)
        serializer = ParadigmSerializer(paradigm,
                                        context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ParadigmUpdateView(APIView):
    """
    Update the paradigm instance.
    """
    def put(self, request, pk):
        paradigm = get_object_or_404(Paradigm, pk=pk)
        data = request.data
        serializer = ParadigmSerializer(paradigm,
                                        data=data,
                                        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParadigmDeleteView(APIView):
    """
    Delete the paradigm instance.
    """
    def delete(self, request, pk):
        paradigm = get_object_or_404(Paradigm, pk=pk)
        paradigm.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LanguageListView(APIView):
    """
    Retrieve the list of languages.
    """

    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages,
                                        many=True,
                                        context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class LanguageCreateView(APIView):
    """
    Create the language instance.
    """
    def post(self, request):
        data = request.data
        serializer = LanguageSerializer(data=data,
                                        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageDetailView(APIView):
    """
    Retrieve the language instance.
    """
    def get(self, request, pk):
        language = get_object_or_404(Language, pk=pk)
        serializer = LanguageSerializer(language,
                                        context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LanguageUpdateView(APIView):
    """
    Update the language instance.
    """
    def put(self, request, pk):
        language = get_object_or_404(Language, pk=pk)
        serializer = LanguageSerializer(language,
                                        data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LanguageDeleteView(APIView):
    """
    Delete the language instance.
    """
    def delete(self, request, pk):
        language = get_object_or_404(Language, pk=pk)
        language.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProgrammerListView(APIView):
    """
    Retrieve the list of programmers.
    """
    def get(self, request):
        programmers = Programmer.objects.all()
        serializer = ProgrammerSerializer(programmers,
                                          many=True,
                                          context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProgrammerCreateView(APIView):
    """
    Create the programmer instance.
    """
    def post(self, request):
        data = request.data
        serializer = ProgrammerSerializer(data=data,
                                          context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgrammerDetailView(APIView):
    """
    Retrieve the programmer instance.
    """
    def get(self, request, pk):
        programmer = get_object_or_404(Programmer, pk=pk)
        serializer = ProgrammerSerializer(programmer,
                                          context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProgrammerUpdateView(APIView):
    """
    Update the programmer instance.
    """
    def put(self, request, pk):
        programmer = get_object_or_404(Programmer, pk=pk)
        serializer = ProgrammerSerializer(programmer,
                                          data=request.data,
                                          context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProgrammerDeleteView(APIView):
    """
    Delete the programmer instance.
    """
    def delete(self, request, pk):
        programmer = get_object_or_404(Programmer, pk=pk)
        programmer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProgrammerLikesView(APIView):
    """
    Retrieve the number of programmer likes.
    """
    def get(self, request, pk):
        programmer = get_object_or_404(Programmer, pk=pk)
        likes = programmer.number_likes
        return Response(likes, status=status.HTTP_200_OK)


class ProgrammerAddLikeView(APIView):
    """
    Add one like to the programmer.
    """
    def patch(self, request, pk):
        programmer = get_object_or_404(Programmer, pk=pk)
        programmer.add_like()
        serializer = ProgrammerSerializer(programmer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProgrammerRemoveLikeView(APIView):
    """
    Remove one like from the programmer.
    """
    def patch(self, request, pk):
        programmer = get_object_or_404(Programmer, pk=pk)
        programmer.remove_like()
        serializer = ProgrammerSerializer(programmer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FrameworkListView(APIView):
    """
    Retrieve the list of frameworks.
    """
    def get(self, request):
        frameworks = Framework.objects.all()
        serializer = FrameworkSerializer(frameworks,
                                         many=True,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FrameworkCreateView(APIView):
    """
    Create the framework instance.
    """
    def post(self, request):
        data = request.data
        serializer = FrameworkSerializer(data=data,
                                         context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FrameworkDetailView(APIView):
    """
    Retrieve the framework instance.
    """
    def get(self, request, pk):
        framework = get_object_or_404(Framework, pk=pk)
        serializer = FrameworkSerializer(framework,
                                         context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FrameworkUpdateView(APIView):
    """
    Update the framework instance.
    """
    def put(self, request, pk):
        framework = get_object_or_404(Framework, pk=pk)
        serializer = FrameworkSerializer(framework,
                                         data=request.data,
                                         context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FrameworkDeleteView(APIView):
    """
    Delete the framework instance.
    """
    def delete(self, request, pk):
        framework = get_object_or_404(Framework, pk=pk)
        framework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)