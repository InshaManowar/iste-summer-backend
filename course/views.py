from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from course.models import Category, Organiser, Submission, Task, Resources
from rest_framework.response import Response
from .serializers import CategorySerializer, OrganiserSerializer, TaskSerializer, SubmissionSerializer, ResourcesSerializer
from accounts.utils import get_user

from .models import STATUS_PUBLISH

@api_view(['GET'])
def category_view(request):
    category=Category.objects.all()
    context={}
    category_serializer=CategorySerializer(category, many=True)
    context['status']='successful'
    context['category']=category_serializer.data
    serializer=category_serializer.data
    return Response(context)

@api_view(['GET'])
def task_view(request):
    task=Task.objects.filter(status=STATUS_PUBLISH)
    print(task)
    context={}
    serializer=TaskSerializer(task, many=True,context={'account':get_user(request)})
    context['status']='successful'
    context['task']=serializer.data
    return Response(context)

@api_view(['GET'])
def resources_view(request):
    resources=Resources.objects.all()
    serializer=ResourcesSerializer(resources, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def submission_view(request):
    submission=Submission.objects.all()
    serializer=SubmissionSerializer(submission, many=True)
    return Response(serializer.data)

