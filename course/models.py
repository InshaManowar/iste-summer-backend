from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from shortuuidfield import ShortUUIDField
from accounts.models import Account


def upload_location(instance, filename, *kwargs):
	file_path = f'task/{instance.category.title}/{filename}'.format(
     pdf_title=str(instance.category), filename=filename)
	return file_path



def upload_location_submission(instance, filename, *kwargs):
    file_path=f'submissions/{instance.account.email}/{filename}'.format(
        pdf_title=str(instance.account), filename=filename
    )
    return file_path


STATUS_DRAFT=0
STATUS_PUBLISH=1

STATUS = (
    (STATUS_DRAFT,"Draft" ),
    (STATUS_PUBLISH,"Publish")
)

class Category(models.Model):
    title=models.CharField(max_length=100)
    short_description=models.TextField(default='')
    startdate=models.DateTimeField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    class Meta:
        ordering=['startdate']
        verbose_name_plural='Categories'
        
    def __str__(self):
        return self.title
    
    
class Organiser(models.Model): #under category
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    name=models.CharField(max_length=150)
    contact=models.CharField(max_length=14)
    
    def __str__(self):
        return self.name


class Task(models.Model): #under category
    uuid= ShortUUIDField(unique=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True, default=None)
    pdf_file= models.FileField(upload_to=upload_location, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    status= models.IntegerField(choices = STATUS, default=0)
    start_date= models.DateTimeField(verbose_name='start_date')
    last_date= models.DateTimeField(verbose_name='last_date', blank=True, null=True)
    
    def __str__(self):
        return self.category.title +"--->"+self.title
    
class Resources(models.Model): #under tasks
    task=models.ForeignKey(Task, on_delete=models.CASCADE)
    video_link=models.URLField()
    video_title=models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural=verbose_name='Resources'

class Submission(models.Model):
    task=models.ForeignKey(Task, related_name='assigned', on_delete=models.CASCADE)
    account=models.ForeignKey(Account, on_delete=models.CASCADE)
    file=models.FileField(
        upload_to=upload_location_submission, 
                          #validators=[FileExtensionValidator(allowed_extensions=['zip'])]
                        )
    comments=models.TextField(blank=True, null=True)
    date=models.DateTimeField(verbose_name='submit_date', auto_now_add=True, null=True)
    def __str__(self):
        return self.task.title+'--->'+self.account.first_name
    
    
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)
pre_save.connect(pre_save_blog_post_receiver, sender=Category)



