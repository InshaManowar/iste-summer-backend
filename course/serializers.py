from rest_framework import serializers
from course.models import Submission, Category, Task, Resources, Organiser
from . import models


class OrganiserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Organiser
        fields=('name','contact')
  
class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resources
        fields=('video_title','video_link')
    
        
class CategorySerializer(serializers.ModelSerializer):
    organisers = OrganiserSerializer(many=True, read_only=True,source='organiser_set')

    class Meta:
        model=Category
        fields=('title', 'short_description','startdate','organisers')
    
    
class TaskSerializer(serializers.ModelSerializer):
    resources=ResourcesSerializer(many=True, read_only=True, source='resources_set')
    category=serializers.StringRelatedField()
    submission=serializers.SerializerMethodField()
    class Meta:
        model=Task
        fields=('uuid','title','description','pdf_file','start_date','last_date','last_date','resources','category','submission',)
        
    def get_submission(self,obj):
        submissions=Submission.objects.filter(task=obj, account=self.context['account'])
        
        if submissions.exists():
            submission_serializer=SubmissionSerializer(submissions,many=True)
            return submission_serializer.data
            
        else:
            return None
        
    def to_representation(self, instance):
        rep = super(TaskSerializer, self).to_representation(instance)
        rep['category'] = instance.category.title
        return rep
    
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Submission
        fields=('comments','date','file')

