from django.db import models


# Create your models here.
class blog(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
