from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    image = models.ImageField(upload_to='fruit_images/')
    prediction = models.CharField(max_length=200, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
