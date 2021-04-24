from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account
from course.models import Submission

class SubmissionAdmin(admin.StackedInline):
    model=Submission

class AccountAdmin(UserAdmin):
    ordering=['email'] #this was defined in the parent class
    fieldsets = [
        (('Login Information'), {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name','registration_number')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_admin','is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    ]

    add_fieldsets = [
        ('Enter this basic information', {
            'classes': ('wide',),
            'fields': ( 'password1', 'password2','email'),
        }),
    ]
    list_display = ('email', 'date_joined', 'last_login', 'is_active', 'is_staff',)
   # ordering = ('-is_shop','is_active')
    search_fields=['email']
    inlines=[SubmissionAdmin]




# class AccountAdmin(UserAdmin):
#     list_display = ('email', 'username', 'date_joined', 'last_login', 'is_active', 'is_staff',)
#     search_fields = ['email', 'username', 'first_name']
#     readonly_fields = ('date_joined', 'last_login')
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()
#     inlines=[SubmissionAdmin]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Account, AccountAdmin)
