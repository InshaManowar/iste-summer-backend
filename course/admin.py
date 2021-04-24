

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from course.models import Submission, Category, Task, Resources, Organiser


class TaskAdmin(admin.StackedInline):
    model=Task
    
class OrganiserAdmin(admin.StackedInline):
    model=Organiser
    
class SubmissionAdmin(admin.StackedInline):
    model=Submission

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'startdate',)
    inlines=[OrganiserAdmin, TaskAdmin]

class ResourcesAdmin(admin.StackedInline):
    model=Resources
    

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines=[SubmissionAdmin, ResourcesAdmin]
    
@admin.register(Organiser)
class OrganiserAdmin(admin.ModelAdmin):
    pass

@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
