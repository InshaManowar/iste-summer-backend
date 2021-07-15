from rest_framework import serializers
from course.models import Category, Task, Resources, Organiser, Submission


class OrganiserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Organiser
        fields = ('name', 'contact')

    def get_name(self, obj):
        return obj.account.first_name + " " + obj.account.last_name


class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = ('video_title', 'video_link')


class TaskSerializer(serializers.ModelSerializer):
    resources = ResourcesSerializer(
        many=True, read_only=True, source='resources_set')
    submission = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('uuid', 'title', 'description', 'pdf_file', 'start_date',
                  'last_date', 'resources', 'submission', 'is_github')

    def get_submission(self, obj):
        try:
            submissions = Submission.objects.get(
                task=obj, account=self.context['account'])

            submission_serializer = SubmissionSerializer(submissions)
            return submission_serializer.data
        except:
            return None


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'slug', 'short_description',
                  'startdate')


class ProfileSerializer(serializers.ModelSerializer):
    count_assigned = serializers.SerializerMethodField()
    count_completed = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('title', 'slug', 'short_description',
                  'startdate', 'count_assigned', 'count_completed')

    def get_count_assigned(self, obj):
        return Task.objects.filter(category=obj).count()

    def get_count_completed(self, obj):
        return Submission.objects.filter(task__category=obj, account=self.context['account']).exclude(comments=None).count()


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('comments', 'date', 'file', 'github_link')
