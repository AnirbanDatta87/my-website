from django.db import models
from django.urls import reverse


class Certificate(models.Model):

    title = models.CharField(max_length=100)
    tagline = models.TextField()
    content = models.TextField()
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title
