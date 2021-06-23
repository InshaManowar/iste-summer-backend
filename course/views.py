from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from course.models import Category, Organiser, Submission, Task, Resources
from rest_framework.response import Response
from .serializers import CategorySerializer, OrganiserSerializer, SubmissionSerializer, TaskSerializer, ResourcesSerializer, ProfileSerializer
from accounts.utils import get_user
from rest_framework.permissions import IsAuthenticated
from .models import STATUS_PUBLISH
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage

from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser

from .serializers import serializers

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_view(request):
    category=Category.objects.all()
    context={}
    category_serializer=CategorySerializer(category, many=True)
    context['status']='successful'
    context['count']=category_serializer.data
    return Response(context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    category=Category.objects.all()
    context={}
    profile_serializer=ProfileSerializer(category, many=True, context={'account':get_user(request)}) #TODO: Pass context of user object into serializer
    context['count']=profile_serializer.data
    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_view(request, slug):
    task=Task.objects.filter(status=STATUS_PUBLISH, category__slug=slug)
    print(task)
    context={}
    serializer=TaskSerializer(task, many=True,context={'account':get_user(request)})
    context['status']='successful'
    context['tasks']=serializer.data

    return Response(context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resources_view(request):
    resources=Resources.objects.all()
    serializer=ResourcesSerializer(resources, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def submission_view(request):
    submission=Submission.objects.all()
    serializer=SubmissionSerializer(submission, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submission(request):
    #folder = 'submissions/'
    #serializer = SubmissionSerializer(data=request.data)
    context={}
    try:
        task=Task.objects.get(uuid=request.data.get('uuid'))
        submission=Submission.objects.create(
            task=task,
            account=get_user(request),
            file=request.FILES.get('file')   
        )
        context['status']='successful'
    
    except:
        context['status']='unsuccessful'
        context['error']='UUID Invalid'
    return Response(context)
   # if request.method == 'POST' and request.FILES['file']:
    #     file = request.data.get('file')
    #     serializer.save(user=request.user)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    