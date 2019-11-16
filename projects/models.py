from django.db import models
# Importing the User model from Django Default Models.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class Project(models.Model):

    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Python', 'Python'),
        ('Django', 'Django'),
        ('AI', 'AI'),
        ('ML', 'ML'),
        ('Analytics', 'Analytics'),
        ('DS', 'DS'),
    ]

    title = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='general')
    tagline = models.TextField()
    content = RichTextUploadingField(blank=True, null=True)
    thumbnail = models.ImageField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-detail', kwargs={'pk': self.pk})
