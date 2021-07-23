

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from course.models import Submission, Category, Task, Resources, Organiser


class ResourcesAdmin(admin.StackedInline):
    model = Resources
    extra = 1

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.category.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.category.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True

    def has_add_permission(self, request, obj=None):
        if obj:
            if obj.category.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'start_date',
                    'last_date', 'pdf_file', )

    list_filter = ['category__title']

    inlines = [ResourcesAdmin]

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.category.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True

    def has_add_permission(self, request, obj=None):
        if obj:
            if obj.category.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.category.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True


class TaskStackedAdmin(admin.StackedInline):
    model = Task
    list_display = ('category', 'status', 'start_date',
                    'last_date', 'pdf_file',)

    extra = 1

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True

    def has_add_permission(self, request, obj):
        if obj:
            if obj.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'startdate',)
    inlines = [TaskStackedAdmin]

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True


@admin.register(Organiser)
class OrganiserAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

    def name(self, obj):
        return obj.account.first_name + " "+obj.account.last_name

    def category(self, obj):
        return obj.category.titles


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['category', 'task', 'name', ]
    search_fields = ['task__category__title', 'task__title',
                     'account__first_name', 'account__last_name']
    list_filter = ['task__category__title', ]
    readonly_fields = ['task', 'account', 'file', 'date', 'github_link']

    def category(self, obj):
        return obj.task.category.title

    def task(self, obj):
        return obj.task.title

    def name(self, obj):
        return obj.account.first_name + " "+obj.account.last_name

    def has_change_permission(self, request, obj=None):
        if obj:
            if obj.task.category.organiser_set.filter(account=request.user).exists():
                return True
            else:
                return False
        return True
