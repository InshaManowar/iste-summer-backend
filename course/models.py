from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

from django.core.validators import FileExtensionValidator
from shortuuidfield import ShortUUIDField
from accounts.models import Account
from tinymce.models import HTMLField

from .utils import Email


def upload_location(instance, filename, *kwargs):
    file_path = f'task/{instance.category.title}/{filename}'.format(
        pdf_title=str(instance.category), filename=filename)
    return file_path


def upload_location_submission(instance, filename, *kwargs):
    file_path = f'submissions/{instance.account.email}/{filename}'.format(
        pdf_title=str(instance.account), filename=filename
    )
    return file_path


STATUS_DRAFT = 0
STATUS_PUBLISH = 1

STATUS = (
    (STATUS_DRAFT, "Draft"),
    (STATUS_PUBLISH, "Publish")
)


class Category(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.TextField(default='')
    startdate = models.DateTimeField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    icon = models.ImageField(null=True, upload_to='icons')

    class Meta:
        ordering = ['startdate']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Organiser(models.Model):  # under category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    account = models.ForeignKey(
        to=Account, on_delete=models.CASCADE)
    contact = models.CharField(max_length=14)

    def __str__(self):
        return self.account.first_name + " " + self.account.last_name


class Task(models.Model):  # under category
    uuid = ShortUUIDField(unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    title = models.CharField(max_length=100)
    description = HTMLField(blank=True, default=None)
    pdf_file = models.FileField(upload_to=upload_location, validators=[
                                FileExtensionValidator(allowed_extensions=['pdf'])])
    status = models.IntegerField(choices=STATUS, default=0)
    start_date = models.DateTimeField(verbose_name='start_date')
    last_date = models.DateTimeField(
        verbose_name='last_date', blank=True, null=True)
    is_github = models.BooleanField(
        default=False, verbose_name='If you want the participant to provide a GitHub link please select this', )

    def __str__(self):
        return self.category.title + "--->"+self.title


class Resources(models.Model):  # under tasks
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    video_link = models.URLField()
    video_title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = verbose_name = 'Resources'


class Submission(models.Model):
    task = models.ForeignKey(
        Task, related_name='assigned', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=upload_location_submission,
        null=True,
        default=None,
        blank=True
    )
    comments = models.TextField(null=True)
    date = models.DateTimeField(
        verbose_name='submit_date', auto_now_add=True, null=True)
    github_link = models.URLField(null=True, default=None, blank=True)

    def __str__(self):
        return self.task.title+'--->'+self.account.first_name

    class Meta:
        unique_together = ['task', 'account']


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


def send_email_after_commenting(sender, instance, *args, **kwargs):
    try:
        old_object = sender.objects.get(pk=instance.pk)
        if old_object.comments is None:
            email = Email()
            email.send_admin_commented_email(instance)
        elif old_object.comments.strip() != instance.comments.strip():
            email = Email()
            email.send_admin_commented_email(instance)
    except Exception as e:
        print(e.__str__())


pre_save.connect(pre_save_blog_post_receiver, sender=Category)
pre_save.connect(send_email_after_commenting, sender=Submission)
