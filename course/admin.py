

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from course.models import Submission, Category, Task, Resources, Organiser


class TaskAdmin(admin.StackedInline):
    model = Task


class OrganiserAdmin(admin.StackedInline):
    model = Organiser


class SubmissionAdmin(admin.StackedInline):
    model = Submission


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'startdate',)
    inlines = [OrganiserAdmin, TaskAdmin]


class ResourcesAdmin(admin.StackedInline):
    model = Resources


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('category', 'status', 'start_date',
                    'last_date', 'pdf_file',)

    inlines = [SubmissionAdmin, ResourcesAdmin]


@admin.register(Organiser)
class OrganiserAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def name(self, obj):
        return obj.account.first_name + " "+obj.account.last_name


@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('video_title', 'task',)


admin.site.register(Category, CategoryAdmin)
