from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageOps

# Create your models here.


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',
                              upload_to='media/profile_pics')
    first_name = models.CharField(blank=True, null=True, max_length=100)
    last_name = models.CharField(blank=True, null=True, max_length=100)
    bio = models.CharField(blank=True,
                           null=True,
                           max_length=10000,
                           default=None)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        cropped_img = ImageOps.fit(img, (300, 300),
                                   method=0,
                                   bleed=0.0,
                                   centering=(0.5, 0.5))
        cropped_img.save(self.image.path)
