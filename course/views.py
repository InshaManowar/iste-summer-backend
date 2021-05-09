from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView
from course.models import Category, Organiser, Submission, Task, Resources
from rest_framework.response import Response
from .serializers import CategorySerializer, OrganiserSerializer, TaskSerializer, SubmissionSerializer, ResourcesSerializer
from accounts.utils import get_user
from rest_framework.permissions import IsAuthenticated
from .models import STATUS_PUBLISH

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def category_view(request):
    category=Category.objects.all()
    context={}
    category_serializer=CategorySerializer(category, many=True)
    context['status']='successful'
    context['count']=category_serializer.data
    return Response(context)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def task_view(request, slug):
    task=Task.objects.filter(status=STATUS_PUBLISH, category__slug=slug)
    print(task)
    context={}
    serializer=TaskSerializer(task, many=True,context={'account':get_user(request)})
    context['status']='successful'
    context['tasks']=serializer.data

    return Response(context)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def resources_view(request):
    resources=Resources.objects.all()
    serializer=ResourcesSerializer(resources, many=True)
    return Response(serializer.data)


@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def submission_view(request):
    submission=Submission.objects.all()
    serializer=SubmissionSerializer(submission, many=True)
    return Response(serializer.data)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def submit_file(request):
    context={}
    try:
        user=get_user(request)
        file=request.FILES.get(user,'file')
        #request.user.save()
        serializer=SubmissionSerializer(many=True)
        context['status']='successful'
        return Response(context)
    except Exception as e:
        context['status']='unsuccessful'
        context['error']=e.__str__()
        print(context)
        return Response(context)
    
    
    
    