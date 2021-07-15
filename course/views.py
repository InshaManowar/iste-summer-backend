from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from course.models import Category, Organiser, Submission, Task, Resources
from accounts.utils import get_user

from .serializers import CategorySerializer, OrganiserSerializer, SubmissionSerializer, TaskSerializer, ResourcesSerializer, ProfileSerializer
from .models import STATUS_PUBLISH
from .serializers import serializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_view(request):
    category = Category.objects.all()
    context = {}
    category_serializer = CategorySerializer(category, many=True)
    context['status'] = 'successful'
    context['count'] = category_serializer.data
    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    category = Category.objects.all()
    context = {}
    profile_serializer = ProfileSerializer(
        category,
        many=True,
        context={
            'account': get_user(request)
        }
    )
    context['status'] = 'successful'
    context['count'] = profile_serializer.data
    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_view(request, slug):
    context = {}
    try:
        category = Category.objects.get(slug=slug)
        task = Task.objects.filter(status=STATUS_PUBLISH, category__slug=slug)

        serializer = TaskSerializer(task, many=True, context={
                                    'account': get_user(request)})
        context['status'] = 'successful'
        context['tasks'] = serializer.data
        context['category_title'] = category.title
        context['organisers'] = OrganiserSerializer(
            category.organiser_set.all(), many=True,).data
    except Exception as e:
        print(e)
        context['status'] = 'unsuccessful'
        context['error'] = 'invalid slug'

    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resources_view(request):
    resources = Resources.objects.all()
    serializer = ResourcesSerializer(resources, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def submission_view(request):
    submission = Submission.objects.all()
    serializer = SubmissionSerializer(submission, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submission(request):
    context = {}
    try:
        task = Task.objects.get(uuid=request.data.get('uuid'))
        submission = Submission.objects.create(
            task=task,
            account=get_user(request),
            file=request.FILES.get('file', None),
            github_link=request.data.get('github_link', None)
        )
        context['status'] = 'successful'
        context['file'] = submission.file.url if not task.is_github else submission.github_link

    except Exception as e:
        context['status'] = 'unsuccessful'
        context['error'] = e.__str__()
    return Response(context)


# views for main website:
